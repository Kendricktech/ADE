from django.urls import path
from .views import RegisterView, LoginView, CustomLogoutView, UpdateUserView, ProfileView
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('update/', UpdateUserView.as_view(), name='update'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Password Reset URLs using your custom templates
    path('password_reset/', 
         PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             success_url='/accounts/password_reset_done/'
         ), 
         name='password_reset'),
         
    path('password_reset_done/',
         PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
         
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url='/accounts/reset/done/'
         ),
         name='password_reset_confirm'),
         
    path('reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
