from django.contrib import admin
from django.urls import path,include
from .views import register,login,custom_logout,update_user,profile_view

app_name='accounts'
urlpatterns = [
   path('register/',register,name='register'),
   path('login/',login,name='login'),
   path('logout',custom_logout,name='logout'),
   path('update/',update_user,name='update'),
       path('profile/', profile_view, name='profile'),
]
