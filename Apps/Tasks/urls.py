from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.sign_up, name="signup"),
    path('logout/', views.log_out, name="logout"),
    path('login/', views.log_in, name="login"),
    path('deletetask/<int:task_id>/', views.delete_task, name="delete_task"),
    path('updatetask/<int:task_id>/', views.update_task, name="update_task"),
    path('markascomplete/<int:task_id>/', views.mark_as_complete, name="mark_as_complete"),
    path('tasks/', views.tasks, name="tasks"),
]
