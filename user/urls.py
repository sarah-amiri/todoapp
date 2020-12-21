from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserCreateAPIView, UserRetrieveUpdateAPIView, LogoutView


urlpatterns = [
    path('', UserRetrieveUpdateAPIView.as_view(), name='get-update-user'),
    path('register/', UserCreateAPIView.as_view(), name='register-user'),
    path('obtain_token/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh_token')
]
