from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from .forms import HomeForm, UtilityForm
from login.models import *
from home.models import *
from .models import *
from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.defaulttags import register
#초대 코드 생성
import uuid
import codecs
import base64



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def nav_notice(request):
    current_user = request.user
    a = Notice.objects.filter(receive_user=current_user)
    notice_cnt = Notice.objects.filter(receive_user=current_user).count()
    print(notice_cnt)
    notices = Notice.objects.filter(receive_user=current_user)
    return notice_cnt, notices 


#집 등록 form - 초대 링크 검색
@csrf_exempt
@login_required
def knock_link_search(request):
    req = json.loads(request.body)
    link_input = req['link_input']
    link_input = link_input.split('/')
    code = link_input[-1] 
    home_pk = link_input[-2]
    
    if(Home.objects.filter(id=home_pk, invite_link=code).exists()):
        is_exist = True
    else:
        is_exist = False
    return JsonResponse({'is_exist': is_exist })
    
#초대 링크 페이지
def invite_link(request, link, pk):
    home = get_object_or_404(Home, invite_link=link, id=pk)
    if request.user.is_authenticated:
        knock = Knock.objects.filter(user=request.user)
    else:
        knock = None
    
    if request.user.is_authenticated:
        notice_cnt, notices = nav_notice(request)
        ctx = {
            'home' : home,
            'knock' : knock,
            'notice_cnt' : notice_cnt,
            'notices' : notices,
        }
    else:
        ctx = {
            'home' : home,
            'knock' : knock,
        }
    return render(request, 'setting/invite_link.html', context=ctx)

#룸메이트 취소
@csrf_exempt
@login_required
def invite_cancel(request):
    req = json.loads(request.body)
    user_id = req['invite_cancel_id']
    receive_user = User.objects.get(pk=user_id)
    Invite.objects.filter(receive_user=receive_user, home=request.user.home).delete()
    return JsonResponse({'id': user_id })
    
#룸메이트 목록
@login_required
def roommate_list(request):
    roommates = User.objects.filter(home=request.user.home)
    roommates = roommates.exclude(nick_name=request.user.nick_name)
    invites = Invite.objects.filter(home=request.user.home)
    
    invite_users = []
    for invite in invites:
        if invite.is_accepted is False:
            invite_users.append(User.objects.get(nick_name=invite.receive_user.nick_name))
            
    roommate_titles = {}
    
    roommate_ratio = {}
    today = datetime.now()
    #전체 달성률
    today_string = f'{today.year}-{today.month}-{today.day}'
    total_todos = Todo.objects.filter(home = request.user.home, date = today_string)
    complete_total_todos = total_todos.filter(is_done=True)
    if total_todos.count() == 0:
        total_compelete_ratio = 0
    else:
        total_compelete_ratio = complete_total_todos.count() / total_todos.count()
        
    for roommate in roommates:
        roommate_titles[roommate.nick_name] = Title.objects.filter(user=roommate)
    
        #룸메이트 달성률
        user_todos = total_todos.filter(user=roommate)
        complete_user_todos = total_todos.filter(is_done = True, user=roommate)
        if user_todos.count() == 0:
            user_compelete_ratio = 0
        else:
            user_compelete_ratio = complete_user_todos.count() / user_todos.count()
            
        roommate_ratio[roommate.nick_name] = int(user_compelete_ratio * 100)
    
    notice_cnt, notices = nav_notice(request)
    ctx = {
        'roommates' : roommates,
        'invite_users' : invite_users,
        'roommate_titles' : roommate_titles,
        'roommate_ratio' : roommate_ratio,
        'total_complete_ratio' : int(total_compelete_ratio * 100),
        'notice_cnt' : notice_cnt,
        'notices' : notices,
    }
    return render(request, 'setting/roommate_list.html', context=ctx)

#집 등록
@csrf_exempt
@login_required
def check_homename(request):
    req = json.loads(request.body)
    home_name = req['home_name']
    if( Home.objects.filter(name=home_name).exists() ):
        return JsonResponse({'is_available' : False, 'input_name': home_name })
    else:
        return JsonResponse({'is_available' : True, 'input_name': home_name })

def create_invite_link():
    link = codecs.encode(uuid.uuid4().bytes, "base64").rstrip()
    link = base64.urlsafe_b64encode(link).decode()[:13]
    return link

@login_required
def myhome_register(request):
    if request.method == 'POST':
        home_form = HomeForm(request.POST)
        utility_form = UtilityForm(request.POST)
        if home_form.is_valid() and utility_form.is_valid():
            print("post")
            current_home = Home()
            current_home.name = home_form.cleaned_data['name']
            
            if(request.POST.get('utility_or_rent') == "월세"):
                print("here")
                current_home.is_rent = True
                current_home.rent_month = home_form.cleaned_data['rent_month']
                current_home.rent_date = home_form.cleaned_data['rent_date']
        
            else:
                current_home.is_rent = False
                current_home.rent_month = 1
                current_home.rent_date = 1
            
            current_home.invite_link = create_invite_link()
            current_home.save()
            request.user.home = current_home
            request.user.save()
            
            #집이 생겼으므로 노크했던 기록은 삭제
            Knock.objects.filter(user=request.user).delete()
            
            #공과금
            utility_name_list = request.POST.getlist('utility_name')
            utility_month_list = request.POST.getlist('utility_month')
            utility_date_list = request.POST.getlist('utility_date')
            for i in range(len(utility_name_list)):
                Utility.objects.create(home = current_home, 
                                    name = utility_name_list[i], 
                                    month = utility_month_list[i],
                                    date = utility_date_list[i])
            #거주 기록
            LiveIn.objects.create(user = request.user, home = current_home)
            
            #기본 ToDo 카테고리
            TodoCate.objects.create(home = current_home, name="빨래")
            TodoCate.objects.create(home = current_home, name="청소")
            
            #기본 생활수칙 카테고리
            LivingRuleCate.objects.create(home = current_home, name = "생활패턴")
            LivingRuleCate.objects.create(home = current_home, name = "돈")
            LivingRuleCate.objects.create(home = current_home, name = "생필품")
            LivingRuleCate.objects.create(home = current_home, name = "다른 사람 초대")
            LivingRuleCate.objects.create(home = current_home, name = "기타")
            
            return redirect('setting:myhome_detail')
    else: #get
        print("get")
        if(Knock.objects.filter(user=request.user).exists()):
            knock =  Knock.objects.get(user=request.user)
            notice_cnt, notices = nav_notice(request)
            ctx = {
                'knock' : knock,
                'notice_cnt' : notice_cnt,
                'notices' : notices,
            }
            return render(request, 'setting/myhome_form.html', ctx)
        
        return render(request, 'setting/myhome_form.html')

# 집 디테일
@login_required
def myhome_detail(request):
    current_user = request.user
    current_home = current_user.home
    utilities = Utility.objects.filter(home=current_home) # 본인 포함
    current_roommates = User.objects.filter(home=current_home) # 본인 포함
    knocks = Knock.objects.filter(receive_home=current_home)
    notice_cnt, notices = nav_notice(request)

    ctx = {
        'home_name' : current_home.name,
        'is_rent' : current_home.is_rent,
        'rent_date' : current_home.rent_date,
        'rent_month' : current_home.rent_month,
        'utilities' : utilities,
        'roommates' : current_roommates,
        'knocks' : knocks,
        'notice_cnt' : notice_cnt,
        'notices' : notices,
    }
    return render(request, 'setting/myhome_detail.html', context=ctx)

#집 업데이트
@csrf_exempt
@login_required
def myhome_update(request):
    req = json.loads(request.body)
    home_name = req['home_name']
    is_rent = req['is_rent']
    rent_month = req['rent_month']
    rent_date = req['rent_date']
    utility_name_list = req['utility_name']
    utility_month_list = req['utility_month']
    utility_date_list = req['utility_date']
    
    current_home = Home.objects.filter(name=request.user.home.name)
    if(is_rent):
        current_home.update(name=home_name, rent_month=rent_month, rent_date=rent_date, is_rent=is_rent)
    else:
        current_home.update(name=home_name, rent_month=1, rent_date=1, is_rent=is_rent) # 1개월마다 1일을 default값으로.

    #공과금
    #업데이트가 복잡하므로 어차피 몇 안되는거 그냥 다 삭제하고 생성    
    Utility.objects.filter(home=request.user.home).delete()
    for i in range(len(utility_month_list)):
        Utility.objects.create(home=request.user.home, name=utility_name_list[i], month=utility_month_list[i], date=utility_date_list[i])
        
    return JsonResponse({ 'home_name' : home_name })


#노크 승낙
@csrf_exempt
@login_required
def accept_knock(request):
    req = json.loads(request.body)
    user_id = req['user_id']
    user = get_object_or_404(User, id=user_id)
    user.home = request.user.home
    user.save()
    
    LiveIn.objects.create(user = user, home = request.user.home)
    Knock.objects.filter(user=user).delete()
    #알림 삭제
    Notice.objects.filter(receive_user=request.user, link="/setting/myhome/detail/").delete()

    if user.profile_img :
        profile = user.profile_img.url
    else :
        profile = ""
        
    return JsonResponse({ 
        'user_name' : user.nick_name,
        'profile': profile,
    })

#노크 거절
@csrf_exempt
@login_required
def reject_knock(request):
    req = json.loads(request.body)
    user_id = req['user_id']
    user = get_object_or_404(User, id=user_id)
    
    Knock.objects.filter(user=user).delete()
    #알림 삭제
    Notice.objects.filter(receive_user=request.user, link="/setting/myhome/detail/").delete()

    return JsonResponse({'success':True})


#(유저가)노크 취소하기
@login_required
def knock_cancel(request):
    Knock.objects.filter(user=request.user).delete()
    
    return redirect('setting:myhome_register')

#노크하기
@csrf_exempt
@login_required
def knock_home(request):
    req = json.loads(request.body)
    homename = req['homename']
    if(homename==None):
        return redirect('setting:myhome_register')
    
    home = get_object_or_404(Home, name=homename)
    Knock.objects.get_or_create(user=request.user, receive_home=home) #유저는 집 하나에만 노크할 수 있음
    #알림에 저장. 집 멤버들에게 모두 알림을 보냄

    for user in User.objects.filter(home=home):
        content = home.name + "에 노크가 들어왔습니다."
        Notice.objects.create(receive_user=user, content=content, link="/setting/myhome/detail/")

    return JsonResponse({'success':True})

#초대링크로 노크
@csrf_exempt
@login_required
def link_knock(request):
    req = json.loads(request.body)
    homename = req['home_name']
    
    home = get_object_or_404(Home, name=homename)
    Knock.objects.get_or_create(user=request.user, receive_home=home) #유저는 집 하나에만 노크할 수 있음
    
    for user in User.objects.filter(home=home):
        content = home.name + "에 노크가 들어왔습니다."
        Notice.objects.create(receive_user=user, content=content, link="/setting/myhome/detail/")

    return JsonResponse({'success':True})

#집 검색하기
@csrf_exempt
@login_required
def search_home(request):
    req = json.loads(request.body)
    search_word = req['search_word']
    
    #db에서 search_word와 일치하는 탑4 유저 검색
    homes = Home.objects.filter(name__startswith=search_word)[:10]
    search_list = []
    for home in homes :
        search_list.append({'homename' : home.name})
    
    return JsonResponse( { "home_list" : search_list } )


#초대하기
@csrf_exempt
@login_required
def invite_roommate(request):
    req = json.loads(request.body)
    invite_list = req['invite_list']
    # 룸메이트 초대 db 저장
    for nickname in invite_list:
        user = User.objects.get(nick_name=nickname)
        Invite.objects.create(home=request.user.home, receive_user=user)
        content = user.nick_name + "님에게 초대장이 도착했습니다."
        #알림에 저장
        Notice.objects.create(receive_user=user, content=content, link="/mypage/")
        
        
    return JsonResponse({'success':True})

#초대 검색
@csrf_exempt
@login_required
def search_user(request):
    req = json.loads(request.body)
    search_word = req['search_word']
    
    #검색 단어 필터링 전, 1. 집이 있는 유저 2. 초대한 룸메를 제외시킨다.
    users = User.objects.exclude(home__isnull=False)
    invites = Invite.objects.filter(home=request.user.home)    
    invite_users = []
    for invite in invites:
        invite_users.append(invite.receive_user.nick_name)
    for invite_user in invite_users:
        users = users.exclude(username=invite_user) # nick_name이 아닌 username.
    
    #db에서 search_word와 일치하는 탑4 유저 검색
    users = users.filter(username__startswith=search_word)[:4]
    search_list = []
    for user in users : # 검색은 아이디, 출력은 닉네임
        if user.profile_img :
            search_list.append({'nickname' : user.nick_name, 'profile' : user.profile_img.url})
        else:
            search_list.append({'nickname' : user.nick_name, 'profile' : ''})
    
    return JsonResponse( { "user_list" : search_list } )

#초대 수락하기
@login_required
def accept_invite(request):
    user = request.user
    invite = get_object_or_404(Invite, receive_user = user)
    invite.is_accepted = True
    invite.save()

    live_in = LiveIn.objects.create(user=user, home=invite.home)
    live_in.save()
    
    user.home = invite.home
    user.save()
    
    #집이 생겼으므로 노크했던 건 삭제
    Knock.objects.filter(user=request.user).delete()
    Invite.objects.filter(receive_user=request.user).delete()

    #알림 삭제
    Notice.objects.filter(receive_user=request.user, link="/mypage/").delete()

    return redirect('login:intro')
