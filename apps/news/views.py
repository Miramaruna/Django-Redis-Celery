from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.conf import settings
from celery import shared_task

from apps.news.models import User, ToDo
from apps.news.serializers import (
    UserRegisterSerializer, UserSerializers, 
    ToDoSerializer, CreateToDoSerializers
)
from apps.news.forms import CustomAuthenticationForm

# Pagination settings
class Pagination(PageNumberPagination):
    page_size = 3
    max_page_size = 10

# Celery tasks
@shared_task
def delete_all_todos_task():
    ToDo.objects.all().delete()
    time.sleep(0.2)
    return redirect('/todo/')

@shared_task
def create_todo_task(user_id, title):
    user = User.objects.get(id=user_id)
    ToDo.objects.create(user=user, title=title)
    time.sleep(0.2)
    return redirect('/todo/')

@shared_task
def mark_completed_task(todo_id):
    todo = ToDo.objects.get(id=todo_id)
    todo.is_completed = True
    todo.save()
    time.sleep(0.2)
    return redirect('/todo/')

@shared_task
def delete_todo_task(todo_id):
    todo = ToDo.objects.get(id=todo_id)
    todo.delete()
    time.sleep(0.2)
    return redirect('/todo/')

# Views
class DeleteAllToDoApiView(ListAPIView):
    queryset = ToDo.objects.all()
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        delete_all_todos_task.delay()
        return Response({"message": "Все записи удалены!"}, status=204)

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

class UserApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]

class TodoCreateApiView(CreateAPIView):
    queryset = ToDo.objects.all()
    serializer_class = CreateToDoSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.user.id
        title = serializer.validated_data.get('title')
        create_todo_task.delay(user_id, title)

class ToDoApiView(ListAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

@login_required
def todohome(request):
    todos = ToDo.objects.filter(user=request.user)[:15]
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            create_todo_task.delay(request.user.id, title)
            return redirect('todo')
    return render(request, 'todo.html', {'todos': todos})

@login_required
def mark_completed(request, todo_id):
    mark_completed_task.delay(todo_id)
    return redirect('todo')

@login_required
def delete_todo(request, todo_id):
    delete_todo_task.delay(todo_id)
    return redirect('todo')

def register(request):
    if request.method == "POST":
        form = UserRegisterSerializer(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('/todo/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterSerializer()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session.set_expiry(60 * 60 * 24 * 30 if remember_me else 0)
            messages.success(request, "Вы успешно вошли!")
            return redirect('todo')
        else:
            messages.error(request, "Неверное имя пользователя или пароль")
    return render(request, 'login.html')

def main(request):
    return render(request, 'home.html')

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        if not form.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        return response

@shared_task
def bar():
    return "Hello, world!"