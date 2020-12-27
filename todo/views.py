from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django.db.models.functions import TruncDate
from django.utils import timezone

from .models import Todo
from .permissions import IsProfileOwner
from .serializers import TodoSerializer


class TodoAPIView(GenericViewSet):
    permission_classes = [IsAuthenticated, IsProfileOwner]
    queryset = Todo.objects.exclude(status=4)
    serializer_class = TodoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_copy(self, request, pk, *args, **kwargs):
        additional_fields = ['status', 'date_created', 'date_modified', 'date_todo', 'date_done']
        todo = self.get_object()

        data = self.get_serializer(todo).data
        new_data = data.copy()
        for field in additional_fields:
            new_data.pop(field)
        new_data['copy_of'] = data.get('id')

        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        try:
            todo = Todo.objects.get(id=pk)
        except Todo.DoesNotExist:
            return Response({'error': 'todo does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(todo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_todo(self, request, pk, *args, **kwargs):
        todo = self.get_object()
        serializer = self.get_serializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def list_filter(self, request, filter, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if filter == 'date':
            if kwargs.get('date', ''):
                date = timezone.datetime(kwargs.get('date')).date()
            else:
                date = timezone.now().date()

            queryset = queryset.annotate(todo_at=TruncDate('date_todo')).filter(user=request.user, todo_at=date)

        elif filter == 'status':
            status_choice = kwargs.get('status', '')
            if  status_choice and status_choice.capitalize() in Todo.get_status_choices_display()[:-1]:
                queryset = queryset.filter(user=request.user, status=status_choice)
            else:
                queryset = queryset.filter(user=request.user)

        else:
            queryset = queryset.filter(user=request.user)

        return Response(TodoSerializer(queryset, many=True).data)


create_todo = TodoAPIView.as_view({'post': 'create'})
todo_detail = TodoAPIView.as_view({'get': 'get_todo', 'post': 'create_copy', 'put': 'update'})
todos = TodoAPIView.as_view({'get': 'list'})
filtered_todos = TodoAPIView.as_view({'get': 'list_filter'})
