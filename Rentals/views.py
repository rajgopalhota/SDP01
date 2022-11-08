from imp import source_from_cache
from tokenize import Name
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime
from .models import  BookedForLater,RidesRightNow
from django.db.models import F

# Create your views here.
def LoginView(request):
    if request.method == 'POST':
        username = request.POST['mail']
        password = request.POST['passwd']
        user = auth.authenticate(username = username, password =password)
        print(username, password)
        if user is not None:
            if user.is_staff == True:
                auth.login(request , user)
                return redirect('/admin')
            auth.login(request , user)
            messages.success(request, 'Welcome Back, Logged In Succeessfully')
            return redirect('/')
        else:
            messages.error(request, 'invalid username or password')
            return redirect("/login")
    else:
        return render(request,'Rentals/login.html')

def Register(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email = request.POST['mail']
        username = request.POST['username']
        password1= request.POST['password1']
        password2= request.POST['password2']
        if password1==password2:
            password = password1
        else:
            messages.info(request, 'Passwords dont match')
        date = datetime.date.today()

        user = User.objects.create_user(first_name = fname, last_name = lname, username = username , password = password , email = email, date_joined = date)
        user.save()
        print('user created')
        return redirect('/login')

    return render(request,'Rentals/register.html')

def LoginOut(request):
    logout(request)
    return redirect('/login')

def BookingHistory(request):
    if request.user.is_authenticated:
        username = request.user.username
        travel_list = BookedForLater.objects.filter(user_name = username)
        return render(request, 'Rentals/history.html', {'travel_list':travel_list})
    messages.error(request, 'Please, Login First!')
    return redirect('/')

def Home(request):
    return render(request, 'Rentals/home.html')

def AboutUs(request):
    return render(request, 'Rentals/about.html')

def Ridenow(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.user.username
            srce = request.POST['o_from']
            dest = request.POST['o_dest']
            type = request.POST['o_optedcar']
            phone = request.POST['o_phone']
            booking = datetime.datetime.today()
            print(srce, dest, type, phone, booking)
            if srce == '' or dest == '' or len(phone)!=10:
                messages.error(request, 'Enter All Fields Properly')
            ride = RidesRightNow(user_name = username, source = srce, destination = dest, cartype = type, phone = phone)
            ride.save()
            messages.success(request, 'Congratulations, Your cab will be arriving soon!')
        return render(request, 'Rentals/OnTheGo.html')
    messages.error(request, 'Please, Login First!')
    return redirect('/')

def Ridelater(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.user.username
            srce = request.POST['s_from']
            dest = request.POST['s_dest']
            sdate = str(request.POST['s_date'])
            stime = str(request.POST['s_time'])
            type = request.POST['s_optedcar']
            phone = request.POST['s_phone']
            booking = datetime.datetime.today()
            print(srce, dest, sdate, stime, type, phone, booking)
            if srce == '' or dest == '' or sdate == '' or stime == '' or len(phone)!=10:
                messages.error(request, 'Enter All Fields Properly')
            else:
                ride = BookedForLater(user_name = username, source = srce, destination = dest,date = sdate,time = stime, cartype = type, phone = phone)
                ride.save()
                messages.success(request, 'Congratulations, Your cab has booked')
        return render(request, 'Rentals/schedule.html')
    messages.error(request, 'Please, Login First!')
    return redirect('/')
    

