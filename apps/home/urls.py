from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('todo/check_catename/', views.check_catename, name='check_catename'),
    path('todo/add_cate/', views.add_cate, name='add_cate'),
    path('todo/delete_cate/', views.delete_cate, name='delete_cate'),

    path('prev_todo/<date>/', views.prev_date_todo, name='prev_date_todo'),

    path('todo/<date>/', views.date_todo, name='date_todo'),
    path('todo/<date>/add/', views.add_todo, name='add_todo'),

    path('todo/<date>/<todo_id>/delete/', views.delete_todo, name='delete_todo'),
    path('todo/<date>/<todo_id>/make-edit-form/', views.make_edit_form, name='make_edit_form'),
    path('todo/<date>/<todo_id>/edit/', views.edit_todo, name='edit_todo'),
    path('todo/<date>/<todo_id>/postpone/', views.postpone_todo, name='postpone_todo'),
    path('todo/<date>/<todo_id>/postpone_today/', views.postpone_today_todo, name='postpone_today_todo'),
    path('todo/<date>/<todo_id>/done/', views.done_todo, name='done_todo'),
    path('todo/<date>/<todo_id>/add_user/', views.add_user, name='add_user'),
    path('todo/<date>/<todo_id>/not_done/', views.not_done_todo, name='not_done_todo'),

    path('living_rules/', views.living_rules, name='living_rules'),
    path('living_rule_new/<int:pk>/', views.living_rule_new, name='living_rule_new'),
    path('<int:pk>/living_rule_edit/', views.living_rule_edit, name='living_rule_edit'),
    path('<int:pk>/living_rule_delete/', views.living_rule_delete, name='living_rule_delete'),
    path('guideline/', views.guideline, name='guideline'),
]