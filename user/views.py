from django.db.models import manager
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django import forms
from user.forms import Video, ManagementFolderForm
from user.models import user_information, friends, management, likess, like, folderss, management_folders,avatars
from django.contrib.auth.decorators import login_required

# Create your views here.

def profile(request):
    user=request.user
    username = user.username
    email = user.email
    password = user.password
    avatar=avatars.objects.filter(user=user)
    if not avatar:
        avatar=avatars.objects.create(user=user)
        avatar.save()
    avatar = user.avatars.avatar
    age1= user_information.objects.filter(email=email).values('age')
    age=age1.first()['age']
    context={
        'username':username,
        'email':email,
        'password':password,
        'age':age,
        'avatar':avatar,
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
    folder_id=request.POST.get('folder_id')
    if folder_id:
        forlder=folderss.objects.get(user=request.user, id=folder_id)
        videos=forlder.video.all()
    else:
        forlder=folderss.objects.filter(user=request.user).first()
        videos=forlder.video.all()
    context={
        'folders':folders,
        'selected_folder':forlder,
        'videos':videos,
    }
    return render(request, 'flavorite.html', context)


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
        folder=ManagementFolderForm(request.POST)
        if form.is_valid() and folder.is_valid():
            title=form.cleaned_data['title']
            description=form.cleaned_data['description']
            video=form.cleaned_data['video']
            user=request.user
            object=management(title=title,description=description,video=video,user=user)
            object.save()
            folder_id=request.POST.get('folder_id')
            if folder_id:
                try:
                    folder = management_folders.objects.get(id=folder_id, user=request.user)
                    folder.videos.add(object)
                except management_folders.DoesNotExist:
                    error_message = "Folder not found or does not belong to the current user."
                    return render(request, 'management.html', {'error1': error_message})
            else:
                new_folder_title=request.POST.get('new_folder_title')
                if folder_id == "" and not new_folder_title:
                    error_message = "You must either select a folder or create a new folder."
                    return render(request, 'management.html', {'error1': error_message})
                if management_folders.objects.filter(user=request.user,title=new_folder_title):
                    error="The folder is already exist"
                    return render(request,'management.html',context={'error':error})
                if new_folder_title:
                    new_folder=management_folders.objects.create(user=request.user,title=new_folder_title)
                    new_folder.videos.add(object)
                    new_folder.save()

            return redirect('user:management')
        if 'delete' in request.POST:
            video_id=request.POST.get('video_id')
            video=management.objects.filter(id=video_id)
            video.delete()
            return redirect('user:management')
    forlder_id1=request.POST.get('folder_id')
    if forlder_id1:
        selected_forlder=management_folders.objects.filter(user=request.user,id=forlder_id1).first()
        videos=selected_forlder.videos.all()
    else:
        selected_forlder=management_folders.objects.filter(user=request.user).first()
        videos=selected_forlder.videos.all()
    folders=management_folders.objects.filter(user=request.user)
    return render(request,'management.html',context={'videos':videos,'folders':folders,'selected_folder':selected_forlder})


def user_friends(request):
    friendss = friends.objects.filter(user=request.user)
    friends_data = [friend.friends for friend in friendss]

    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            target = User.objects.get(email=email)
            context = {'target': target}
            if 'add' in request.POST:
                print("add")
                if not friends.objects.filter(user=request.user, friends=target).exists():
                    friends.objects.create(user=request.user, friends=target)
                    return redirect('user:friends')
                else:
                    context['error2'] = "You already added this person as your friend"
                    return render(request, 'friends.html', context)
            return render(request, 'friends.html', context)

        context = {'error': True}
        return render(request, 'friends.html', context)

    return render(request, 'friends.html', context={'friends': friends_data})
