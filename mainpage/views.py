from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_http_methods
from mainpage.forms import *
from user.forms import Video
from user.models import user_information,management,likes,like,likess
from django import forms
from mainpage.forms import *
from django.contrib.auth.models import User
# Create your views here.
@require_http_methods(['GET','POST'])
def mainpage_template(request):
    return render(request, "default_mainpage.html", )


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
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, "login.html", )

def sign_up(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            print(type(form.cleaned_data))
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            age = form.cleaned_data['age']
            object= user_information(username=username, password=password, email=email, age=age)
            object.save()
            user = User.objects.create_user(username=username, password=password, email=email)
            return redirect('mainpage:sign_in')
        return redirect('mainpage:sign_up')
    return render(request, "sign_up.html")


def sign_out(request):
    logout(request)
    return redirect('mainpage:sign_in')

def Management(request):
    email=request.user.email
    print(email)
    return redirect('mainpage:mainpage')
def user_mainpage(request):
    videos=management.objects.all()
    user=request.user
    if request.method == "POST":
        if 'like' in request.POST:
            video_id=request.POST.get('video_id')
            print(video_id)
            video=management.objects.get(id=video_id)
            print(video)
            print(user)
            oo=likess.objects.create(video=video,user=user)
            return redirect('mainpage:user_mainpage')
    context = {'user':user,'videos':videos}
    return render(request, "user_mainpage.html", context)