from django.db.models import manager
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django import forms
from user.forms import Video
from user.models import user_information,friends,management,likess,like,folderss
from django.contrib.auth.decorators import login_required

# Create your views here.

def profile(request):
    username = request.user.username
    email = request.user.email
    password = request.user.password
    age1= user_information.objects.filter(email=email).values('age')
    age=age1.first()['age']
    context={
        'username':username,
        'email':email,
        'password':password,
        'age':age
    }
    return render(request,'profile.html',context)


def user_flavorite(request):
    default_folder=folderss(user=request.user,title='default')
    correction=folderss.objects.filter(user=request.user,title='default')
    if not correction.exists():
        default_folder.save()
    if 'create_folder' in request.POST:
        title = request.POST.get('title')
        if title:
            new_folder=folderss.objects.create(user=request.user,title=title)
            new_folder.save()
            return redirect('user:flavorite')
    folders = folderss.objects.filter(user=request.user)
    context={
        'folders':folders,
    }
    return render(request,'flavorite.html',context)


def user_likes(request):
    if request.user.is_authenticated:
        likes_videoes=likess.objects.filter(user=request.user)
        if 'delete' in request.POST:
            video_id = request.POST.get('video_id')
            print(video_id)
            video = likes_videoes.filter(id=video_id)
            video.delete()
            return redirect('user:likes')
        context = {'likes_videoes': likes_videoes}
        return render(request, 'likes.html', context)
    return redirect('user:login')

@login_required
def user_management(request):
    if request.method=='POST':
        form=Video(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            title=form.cleaned_data['title']
            description=form.cleaned_data['description']
            video=form.cleaned_data['video']
            user=request.user
            object=management(title=title,description=description,video=video,user=user)
            object.save()
            print("save successfully done")
            return render(request,'management.html',context={'object':object})
        if 'delete' in request.POST:
            video_id=request.POST.get('video_id')
            video=management.objects.filter(id=video_id)
            video.delete()
            return redirect('user:management')
    videos=management.objects.filter(user=request.user)
    print('gg')
    return render(request,'management.html',context={'videos':videos})


def user_friends(request):
    friendss=friends.objects.filter(user=request.user)
    username=[friend.friends.username for friend in friendss]
    useremail=[friend.friends.email for friend in friendss]
    friend=zip(username,useremail)
    print(username)
    print(useremail)
    if request.method=='POST':
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            target=User.objects.get(email=email)
            print(target.username)
            context={'target':target}
            if 'add' in request.POST:
                print("add")
                judgement=True
                if not friends.objects.filter(user=request.user,friends=target).exists():
                    friends.objects.create(user=request.user,friends=target)
                    judgement=False
                    return redirect('user:friends')
                else:
                    context={
                        'target':target,
                        'error2':"You already add this person as your friend"
                    }
                    return render(request,'friends.html',context)
            return render(request,'friends.html',context)
        error= True;
        print(error)
        return  render(request,'friends.html',context={'error':error})
    return render(request,'friends.html',context={'friend':friend})



