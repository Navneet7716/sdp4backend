from django.urls import path

from .views import UserRegistrationView, UserLoginView, UserLogoutView, GoogleSocialAuthView


urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('google/', GoogleSocialAuthView.as_view()),
    path('logout/', UserLogoutView.as_view())
]