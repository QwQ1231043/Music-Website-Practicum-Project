from random import random
import string
import random
from django.http.response import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_http_methods
from mainpage.forms import *
from user.forms import Video
from user.models import user_information, management, likes, like, likess, folderss, favorites, avatars
from django import forms
from mainpage.forms import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
# Create your views here.

def mainpage_template2(request):
    avatar = 'media/avatars/default.jpg'
    videos = management.objects.all().order_by('?')[:10]
    return render(request, "default_mainpage.html", {'videos': videos, 'user': user, 'avatar': avatar})


def sign_in(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)  # Create session and mark user as authenticated
            user=request.user
            avatar=user.avatars.avatar
            return render(request,'user_mainpage.html',{'avatar':avatar,'user':user})
        else:
            print("error")
            return render(request, 'login.html', {'error': 'Invalid credentials, please check your account and password'})
    return render(request, "login.html")

def send_verification(request,email1):
    verification_code = "".join(random.sample(string.digits, 6))
    request.session['verification_code'] = verification_code
    send_mail("Your verification code", message=f"This is your verification code:{verification_code}",
              recipient_list=[email1], from_email='zhengdongyaoo@gmail.com')

def check_verification(request):
    if request.method == "POST":
        entered_code=request.POST.get('verification_code')
        stored_code=request.session.get('verification_code')
        if entered_code == stored_code:
            username = request.session.get('username')
            password = request.session.get('password')
            email = request.session.get('email')
            age = request.session.get('age')
            user = User.objects.create_user(username=username, password=password, email=email)
            user1=  user_information(username=username, password=password, age=age,email=email)
            avatar = avatars.objects.create(user=user)
            avatar.save()
            user.save()
            user1.save()
            return redirect('mainpage:sign_in')
        else:
            error_message="Invalid verification code, please try again"
            return render(request, "send_verification.html", {'error_message': error_message})
    return render(request,'send_verification.html')

def sign_up(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            age = form.cleaned_data['age']
            if User.objects.filter(username=username).exists():
                error_message="This username is already taken"
                error_message1=True
                return render(request, "sign_up.html", {'form': form, 'error_message': error_message,'error_message1': error_message1})
            send_verification(request,email)
            request.session['username']=username
            request.session['email']=email
            request.session['age']=age
            request.session['password']=password
            return redirect('mainpage:check_verification')
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
    videos=management.objects.all().order_by('?')[:8]
    videos_with_likes = []
    for video in videos:
        like_count = likess.objects.filter(video=video).count()
        videos_with_likes.append({'video': video, 'like_count': like_count})
    folders=folderss.objects.filter(user=request.user)
    user=request.user
    avatar=user.avatars.avatar
    liked_videos=likess.objects.filter(user=user).values_list('video',flat=True)
    if request.method == "POST":
        if 'like' in request.POST:
            video_id=request.POST.get('video_id')
            video=management.objects.get(id=video_id)
            if not likess.objects.filter(video=video, user=user).exists():
                likess.objects.create(video=video, user=user)
            return redirect('mainpage:user_mainpage')
        if 'favorite' in request.POST:
            video_id = request.POST.get('video_id')
            video = management.objects.get(id=video_id)
            folder_id = request.POST.get('folder_id')
            folder = folderss.objects.get(id=folder_id, user=user)
            if not folder.video.filter(id=video_id).exists():
                folder.video.add(video)
                folder.save()
            return redirect('mainpage:user_mainpage')
    context = {'user':user,'videos':videos,'folders':folders,'avatar':avatar,'liked_videos':liked_videos,'videos_with_likes':videos_with_likes}
    return render(request, "user_mainpage.html", context)
