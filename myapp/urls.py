from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('login', views.login, name="signin"),
    path('register', views.register, name="signup"),
    path('logout',views.logout, name = "logout"),
    path('welcome',views.welcome, name = "welcome"),
]