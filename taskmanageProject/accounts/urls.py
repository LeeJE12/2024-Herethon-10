from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/success/', views.signup_success, name='signup_success'),
    path('signup/fail/', views.signup_fail, name='signup_fail'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]