from django.urls import path
from apps.news.views import delete_todo_task, create_todo_task, mark_completed_task, todohome, mark_completed, delete_todo, login_view, register, main, CustomLogoutView, mark_uncompleted_task
from django_prometheus import exports

urlpatterns = [
    path('', main, name='home'),  # Главная страница
    path('todo/', todohome, name='todo'),
    path('mark_completed/<int:todo_id>/', mark_completed, name='mark_completed'),
    path('delete_todo/<int:todo_id>/', delete_todo, name='delete_todo'), 
    path("register/", register, name="register"),
    path('login/', login_view, name="login"),
    path('create_todo_task/', create_todo_task, name='create_todo_task'),
    path('metrics/', exports.ExportToDjangoView, name='prometheus-metrics'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('mark_uncompleted_task/<int:todo_id>/', mark_uncompleted_task, name='mark_uncompleted_task'),
]