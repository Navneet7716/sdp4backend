from django.urls import path

from .views import GetUserFiles, UserRegistrationView, UserLoginView, UserLogoutView, GoogleSocialAuthView, UpdateData


urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('google/', GoogleSocialAuthView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('update/', UpdateData.as_view()),
    path('get-user-files/<str:email>', GetUserFiles.as_view()),
]