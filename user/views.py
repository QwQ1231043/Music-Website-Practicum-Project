import os

from django.db.models import manager
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django import forms
from user.forms import Video, ManagementFolderForm, EditProfileForm, changed_data
from user.models import user_information, friends, management, likess, like, folderss, management_folders,avatars, userprofile
from django.contrib.auth.decorators import login_required

# Create your views here.

def profile(request):
    user=request.user
    username = user.username
    email = user.email
    password = user.password
    avatar=avatars.objects.filter(user=user)
    introduction=userprofile.objects.filter(user=user).first()
    if not introduction:
        introduction=userprofile.objects.create(user=user)
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
        'introduction':introduction,
    }
    return render(request,'profile.html',context)


def user_flavorite(request):
    user=request.user
    avatar = user.avatars.avatar
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
        'user':user,
        'avatar':avatar,
    }
    return render(request, 'flavorite.html', context)


def user_likes(request):
    user=request.user
    avatar = user.avatars.avatar
    if request.user.is_authenticated:
        likes_videoes=likess.objects.filter(user=request.user)
        if 'delete' in request.POST:
            video_id = request.POST.get('video_id')
            print(video_id)
            video = likes_videoes.filter(id=video_id)
            video.delete()
            return redirect('user:likes')
        context = {'likes_videoes': likes_videoes,'user':user,'avatar':avatar}
        return render(request, 'likes.html', context)
    return redirect('user:login')

@login_required
def user_management(request):
    user=request.user
    avatar = user.avatars.avatar
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
                    return render(request, 'management.html', {'error1': error_message,'user':user,'avatar':avatar})
            else:
                new_folder_title=request.POST.get('new_folder_title')
                if folder_id == "" and not new_folder_title:
                    error_message = "You must either select a folder or create a new folder."
                    return render(request, 'management.html', {'error1': error_message,'user':user,'avatar':avatar})
                if management_folders.objects.filter(user=request.user,title=new_folder_title):
                    error="The folder is already exist"
                    return render(request,'management.html',context={'error':error,'user':user,'avatar':avatar})
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
        if not selected_forlder:
            management_folders.objects.create(user=request.user,title='default')
            selected_forlder=management_folders.objects.filter(user=request.user).first()
        videos=selected_forlder.videos.all()
    folders=management_folders.objects.filter(user=request.user)
    return render(request,'management.html',context={'videos':videos,'folders':folders,'selected_folder':selected_forlder,'user':user,'avatar':avatar})



def user_friends(request):
    user=request.user
    avatar1 = user.avatars.avatar
    friendss = friends.objects.filter(user=request.user)
    friends_data = []
    for friend in friendss:
        friend_user = friend.friends
        age=user_information.objects.get(email=friend_user.email)
        age=age.age
        try:
            profile = userprofile.objects.get(user=friend_user)
        except userprofile.DoesNotExist:
            profile=userprofile.objects.create(user=friend_user)
        try:
            friend_avatar=avatars.objects.get(user=friend_user)
        except avatars.DoesNotExist:
            friend_avatar=avatars.objects.create(user=friend_user)
        friends_data.append({
            'friend': friend_user,
            'profile': profile,
            'avatar': friend_avatar,
            'age': age,
        })

    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            target = User.objects.get(email=email)
            context = {'target': target,'user':user,'avatar':avatar1}
            if 'add' in request.POST:
                if not friends.objects.filter(user=request.user, friends=target).exists():
                    friends.objects.create(user=request.user, friends=target)
                    return redirect('user:friends')
                else:
                    context['error2'] = "You already added this person as your friend"
                    return render(request, 'friends.html', context)
            return render(request, 'friends.html', context)
        context = {'error': True,'user':user,'avatar':avatar1}
        return render(request, 'friends.html', context)


    return render(request, 'friends.html', context={'friends': friends_data,'user':user,'avatar':avatar1})

def delete_friend(request,friend_id):
    if request.method=="POST":
        friendship = friends.objects.get(user=request.user, friends__id=friend_id)
        friendship.delete()
        return redirect('user:friends')


def edit_profile(request):
    user = request.user
    try:
        avatar = avatars.objects.get(user=user)
    except avatars.DoesNotExist:
        avatar =avatars.objects.create(user=user)
    try:
        user_profile = userprofile.objects.get(user=user)
    except userprofile.DoesNotExist:
        user_profile = userprofile.objects.create(user=user)

    if request.method == 'POST':
        form = changed_data(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            age = form.cleaned_data['age']
            introduction = form.cleaned_data['introduction']
            avatar_file = request.FILES.get('avatar')
            if username:
                user.username = username
                use=user_information.objects.get(email=user.email)
                use.username=username
                use.save()
            if age is not None:
                userInformation=user_information.objects.get(email=user.email)
                userInformation.age = age
                userInformation.save()
            if introduction:
                user_profile.introduction = introduction
            if avatar_file:
                if avatar.avatar and avatar.avatar.name != 'avatars/default.jpg':
                    old_avatar_path = avatar.avatar.path
                    if os.path.exists(old_avatar_path):
                        os.remove(old_avatar_path)
                avatar.avatar = avatar_file
            user.save()
            user_profile.save()
            avatar.save()
            return redirect('user:profile')
    else:
        form = changed_data(initial={
            'username': user.username,
            'age': user_information.age if user_profile else '',
            'introduction': user_profile.introduction if user_profile else '',
        })
    avatar=user.avatars.avatar
    return render(request, 'edit_profile.html', {'form': form, 'avatar': avatar})

def delete_folder(request,folder_id):
    folder=folderss.objects.get(id=folder_id)
    folder.delete()
    return redirect('user:flavorite')

def delete_video_from_folder(request, folder_id, video_id):
    user = request.user
    folder = get_object_or_404(folderss, id=folder_id, user=user)
    video = get_object_or_404(management, id=video_id, user=user)
    folder.video.remove(video)
    return redirect('user:flavorite')