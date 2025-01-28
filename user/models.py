from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class user_information(models.Model):
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    age = models.IntegerField(default=0)

class friends(models.Model):
    user=models.ForeignKey(User,related_name="friendship_set",on_delete=models.CASCADE)
    friends= models.ForeignKey(User, related_name="friendship",on_delete=models.CASCADE)
    class Meta:
        unique_together=('user','friends')

class management(models.Model):
    user=models.ForeignKey(User,related_name="management_set",on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=20000)
    upload_time=models.DateTimeField(auto_now_add=True)
    video=models.FileField(upload_to="videos/")

class likes(models.Model):
    video=models.ForeignKey(management,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    like_time=models.DateTimeField(auto_now_add=True)

class like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    like_time=models.DateTimeField(auto_now_add=True)

class likess(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    video=models.ForeignKey(management,on_delete=models.CASCADE)
    like_time=models.DateTimeField(auto_now_add=True)

class folderss(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    video = models.ManyToManyField(management, blank=True)
    def _str_(self):
        return self.title

class favorites(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    video=models.ManyToManyField(management,blank=True)
    folder=models.ForeignKey(folderss,on_delete=models.CASCADE,default=None)
    add_time=models.DateTimeField(auto_now_add=True)

class management_folders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    videos=models.ManyToManyField(management, blank=True)

class avatars(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    avatar=models.ImageField(upload_to="avatars/",default='avatars/default.jpg')
    def __str__(self):
        return self.user.username

class userprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    age=models.IntegerField(default=0)
    introduction=models.CharField(max_length=500,default='This user is too lazy to leave anything behind.')

class comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.ForeignKey(management, related_name="comments", on_delete=models.CASCADE,default=None)
    comment=models.CharField(max_length=700)
    created_at=models.DateTimeField(auto_now_add=True)
