from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('login/', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('todo/', todo_list, name='todo_list'),  
    path('logout/', logout_view, name='logout'),
    path('tasks/', task_list, name='task_list'),
    path('update-task/<int:task_id>', update_task, name='update_task'),
    path('delete-task/<int:task_id>/', delete_task, name='delete_task'),

]
