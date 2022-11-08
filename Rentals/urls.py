from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.LoginView, name = 'login'),
    path('register/', views.Register, name = 'register'),
    path('ridenow/', views.Ridenow, name = 'ridenow'),
    path('schedule/', views.Ridelater, name = 'schedule'),
    path('', views.Home, name = 'home'),
    path('aboutus/', views.AboutUs, name = 'aboutus'),
    path('history/', views.BookingHistory, name = 'history'),
    path('loginout/', views.LoginOut, name = 'history'),
]
