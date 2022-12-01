from imp import source_from_cache
from tokenize import Name
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import  BookedForLater,RidesRightNow
from django.db.models import F
import math, random, time


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
            context= {'Error':'INVALID CREDENTIALS','Sign':' X'}
            return render(request, 'Rentals/login.html', context)
    else:
        return render(request,'Rentals/login.html')

def Register(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email = request.POST['mail']
        usern = request.POST['username']
        password1= request.POST['password1']
        password2= request.POST['password2']
        if password1==password2:
            password = password1
        else:
            context= {'Error':'Passwords does not match','Sign':' X'}
            return render(request, 'Rentals/register.html', context)
        date = datetime.date.today()
        try:
            user= User.objects.get(username=usern)
            context= {'Error':'The username already taken. Please try another username.','Sign':' X'}
            return render(request, 'Rentals/register.html', context)
        except User.DoesNotExist:
            try:
                user= User.objects.get(email=email)
                context= {'Error':'The email already taken. Please try another email.','Sign':' X'}
                return render(request, 'Rentals/register.html', context)
            except User.DoesNotExist:
                user = User.objects.create_user(first_name = fname, last_name = lname, username = usern , password = password , email = email, date_joined = date)
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

def home(request):
    return render(request, 'Rentals/home.html')

def AboutUs(request):
    return render(request, 'Rentals/about.html')

def Forgot(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user= User.objects.get(email=email)
            email=request.POST['email']
            u = User.objects.get(email = email)
            o=generateOTP()
            u.set_password(o)
            u.save()
            context= {'otp':o}
            html_message = render_to_string('Rentals/otpemail.html', context)
            plain_message = strip_tags(html_message)
            mail = EmailMultiAlternatives(
                #subject
                'OTP VERIFICATION',
                #content
                plain_message,
                #from email
                'taxies24hrs@gmail.com',
                #reciepents
                [email]
            )
            mail.attach_alternative(html_message, "text/html")
            mail.send()
            print("Sent")
            return redirect('/passreset')
        except User.DoesNotExist:
            messages.error(request, ' User Does not exixst...')
    return render(request,'Rentals/forgot.html')
def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

# def send_otp(request, mail):
#     email=request.POST['email']
#     u = User.objects.get(email = mail)
#     o=generateOTP()
#     u.set_password(o)
#     u.save()
#     send_mail('OTP Verification',#subject
#               o, #body
#               'taxies24hrs@gmail.com',#from
#               [mail],#to
#               fail_silently=False,
#               )
#     print("Sent")
#     return redirect('/passreset')
    
def PassReset(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        otp = request.POST['otp']
        pass0 = request.POST['pass']
        pass1 = request.POST['pass1']
        user = auth.authenticate(username = uname, password =otp)
        if user is not None:
            if pass0==pass1:
                u = User.objects.get(username = uname)
                u.set_password(pass0)
                u.save()
                messages.success(request, 'Password changed Successfully...')
                time.sleep(6)
                return redirect('/login')
            messages.error(request, 'Passwords mismatch')
        else:
            messages.error(request, 'Invalid Username or OTP')
    return render(request,'Rentals/passreset.html')

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
            else:
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
                confirmmail(request, srce,dest,sdate,stime)
                messages.success(request, 'Congratulations, Your cab has booked')
        return render(request, 'Rentals/schedule.html')
    messages.error(request, 'Please, Login First!')
    return redirect('/')

def confirmmail(request,srce,dest,sdate,stime):
    email = request.user.email
    print(email)
    # msg = "Source: "+str(srce)+"\n"+"Destination: "+str(dest)+"\n"+"Date of travel: "+str(sdate)+"\n"+"Time: "+str(stime)+"\n"
    context= {'source':srce,'destination':dest, 'date':sdate, 'time': stime}
    html_message = render_to_string('Rentals/confirmemail.html', context)
    plain_message = strip_tags(html_message)
    mail = EmailMultiAlternatives(
        #subject
        'RIDE CONFIRMATION',
        #content
        plain_message,
        #from email
        'taxies24hrs@gmail.com',
        #reciepents
        [email]
    )
    mail.attach_alternative(html_message, "text/html")
    mail.send()
    # send_mail('Ride Confirmation.........',#subject
    #           plain_message, #body
    #           'taxies24hrs@gmail.com',#from
    #           [email],#to
    #           fail_silently=False,
    #           )
    return print("Mail Sent")
    

