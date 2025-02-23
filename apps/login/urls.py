from django.contrib import admin
from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.intro, name='intro'),
    
    #이사가기
    path('leave_home/', views.leave_home, name='leave_home'),
    
    #ajax
    path('mypage/take_prelivingrule/', views.take_prelivingrule, name='take_prelivingrule'),

    #이전집 기록 보기 만들려고 만든 임시 url. 나중에 삭제
    path('mypage/', views.mypage, name='mypage'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user_update/', views.user_update, name='user_update'),
    path('profile_delete/', views.profile_delete, name='profile_delete'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('signup/check_username/', views.check_username, name='check_username'),
    path('signup/check_email/', views.check_email, name='check_email'),
    path('signup/check_nick_name/', views.check_nick_name, name='check_nick_name'),
]