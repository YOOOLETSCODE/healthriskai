from django.urls import path
from . import views 

app_name = "accounts"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginuser, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logoutuser, name='logout'),
    
]
