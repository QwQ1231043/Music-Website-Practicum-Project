from django.db.models import manager
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django import forms
from user.forms import Video
from user.models import user_information,friends,management,likess
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
    return render(request,'flavorite.html')

def user_likes(request):
    likes_videoes=likess.objects.all()
    context={'likes_videoes':likes_videoes}
    return render(request,'likes.html',context)

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
    videos=management.objects.filter(user=request.user)
    print('gg')
    return render(request,'management.html',context={'videos':videos})


def user_friends(request):
    friendss=friends.objects.filter(user=request.user)
    friend_list=[friend.friends.username for friend in friendss]
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
                    return redirect('friends')
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
    return render(request,'friends.html',context={'friend_list':friend_list})