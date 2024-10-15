from django.urls import path
from .views import UserRegisterView, UserLoginView, UserPasswordResetRequestView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('password-reset/', UserPasswordResetRequestView.as_view(), name='password-reseting'),
]
