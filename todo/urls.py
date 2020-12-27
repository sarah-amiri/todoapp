from django.urls import path

from .views import create_todo,todo_detail, todos, filtered_todos

urlpatterns = [
    path('todo/', create_todo, name='todo_create'),
    path('todo/<int:pk>/', todo_detail, name='todo_detail'),
    path('todos/', todos, name='list_todos'),
    path('todos/<str:filter>/', filtered_todos, name='list_filtered_todos')
]