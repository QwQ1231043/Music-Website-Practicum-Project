from django import forms
from django.db import models
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

class MessageForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=120)
    email = forms.CharField(max_length=120)
    age = forms.IntegerField(initial=0)
    def clean(self):
        cleaned_data = super(MessageForm, self).clean()
        cleaned_data1 = self.cleaned_data.get('email')
        exist=  User.objects.filter(email=cleaned_data1).exists()
        if exist:
            print("email already exists")
            raise forms.ValidationError("Email already registered")
        return cleaned_data


class likes(models.Model):
    likes=forms.FileField()



class favorites(models.Model):
    favorites=forms.FileField()