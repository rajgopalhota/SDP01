from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.LoginView, name = 'login'),
    path('register/', views.Register, name = 'register'),
    path('ridenow/', views.Ridenow, name = 'ridenow'),
    path('schedule/', views.Ridelater, name = 'schedule'),
    path('', views.home, name = 'home'),
    path('forgot/', views.Forgot, name = 'forgot'),
    path('passreset/', views.PassReset, name = 'passreset'),
    path('aboutus/', views.AboutUs, name = 'aboutus'),
    path('feedback/', views.Feedback, name = 'feedback'),
    path('history/', views.BookingHistory, name = 'history'),
    path('quickhistory/', views.QuickBookingHistory, name = 'quickhistory'),
    path('loginout/', views.LoginOut, name = 'history'),
    path('history/delete/<int:id>/', views.delete, name='delete'),
    path('quickhistory/delete1/<int:id>/', views.delete1, name='delete1'),
]
