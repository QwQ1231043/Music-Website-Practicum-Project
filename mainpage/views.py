from random import random
import string
import random
from django.http.response import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_http_methods
from mainpage.forms import *
from user.forms import Video
from user.models import user_information,management,likes,like,likess,folderss,favorites
from django import forms
from mainpage.forms import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
# Create your views here.
@require_http_methods(['GET','POST'])
def mainpage_template(request):
    videos = management.objects.all().order_by('?')[:10]
    return render(request, "default_mainpage.html", {'videos':videos})


def sign_in(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)  # Create session and mark user as authenticated
            return render(request,'user_mainpage.html')
        else:
            print("error")
            return render(request, 'login.html', {'error': 'Invalid credentials, please check your account and password'})
    return render(request, "login.html", )

def send_verification(request,email1):
    verification_code = "".join(random.sample(string.digits, 6))
    request.session['verification_code'] = verification_code
    send_mail("Your verification code", message=f"This is your verification code:{verification_code}",
              recipient_list=[email1], from_email='zhengdongyaoo@gmail.com')

def check_verification(request):
    if request.method == "POST":
        entered_code=request.POST.get('verification_code')
        stored_code=request.session.get('verification_code')
        print(entered_code)
        print(stored_code)
        if entered_code == stored_code:
            username = request.session.get('username')
            password = request.session.get('password')
            email = request.session.get('email')
            age = request.session.get('age')
            user = User.objects.create_user(username=username, password=password, email=email)
            user1=  user_information(username=username, password=password, age=age,email=email)
            user.save()
            user1.save()
            return redirect('mainpage:sign_in')
        else:
            error_message="Invalid verification code,please try again"
            return render(request, "send_verification.html", {'error_message': error_message})
    return render(request,'send_verification.html')

def sign_up(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            print(type(form.cleaned_data))
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            age = form.cleaned_data['age']
            if User.objects.filter(username=username).exists():
                error_message="This username is already taken"
                error_message1=True
                return render(request, "sign_up.html", {'form': form, 'error_message': error_message,'error_message1': error_message1})
            object= user_information(username=username, password=password, email=email, age=age)
            object.save()
            send_verification(request,email)
            request.session['username']=username
            request.session['email']=email
            request.session['age']=age
            request.session['password']=password
            return redirect('mainpage:check_verification')
        print(form.errors)
        return render(request, "sign_up.html",{'form':form})
    return render(request, "sign_up.html")


def sign_out(request):
    logout(request)
    return redirect('mainpage:sign_in')

def Management(request):
    email=request.user.email
    print(email)
    return redirect('mainpage:mainpage')
def user_mainpage(request):
    videos=management.objects.all().order_by('?')[:10]
    folders=folderss.objects.filter(user=request.user)

    user=request.user
    if request.method == "POST":
        if 'like' in request.POST:
            video_id=request.POST.get('video_id')
            video=management.objects.get(id=video_id)
            oo=likess.objects.create(video=video,user=user)
            return redirect('mainpage:user_mainpage')
        if 'favorite' in request.POST:
            video_id = request.POST.get('video_id')
            video = management.objects.get(id=video_id)
            folder_id = request.POST.get('folder_id')
            folder = folderss.objects.get(id=folder_id, user=user)
            folder.video.add(video)
            folder.save()
            print(folder)
            print('fuck')
            return redirect('mainpage:user_mainpage')
    print('pass')
    context = {'user':user,'videos':videos,'folders':folders}
    return render(request, "user_mainpage.html", context)