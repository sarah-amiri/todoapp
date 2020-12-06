from django.urls import path

from .views import UserCreateAPIView, UserRetrieveUpdateAPIView


urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register-user'),
    path('<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='get-update-user')
]