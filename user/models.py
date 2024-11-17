from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class user_information(models.Model):
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    email = models.CharField(max_length=120,unique=True)
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

