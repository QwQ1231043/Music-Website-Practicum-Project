from django import forms
from django.db import models
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

class MessageForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=120)
    password2=forms.CharField(max_length=120)
    email = forms.CharField(max_length=120)
    age = forms.IntegerField(initial=0)
    def clean(self):
        cleaned_data = super(MessageForm, self).clean()
        cleaned_data1 = self.cleaned_data.get('email')
        cleaned_data2 = self.cleaned_data.get('password')
        cleaned_data3 = self.cleaned_data.get('password2')
        cleaned_data4 = self.cleaned_data.get('age')
        cleaned_data5 = self.cleaned_data.get('username')
        exist=  User.objects.filter(email=cleaned_data1).exists()
        if User.objects.filter(email=cleaned_data5).exists():
            raise forms.ValidationError("Username already registered")
        if not cleaned_data1 or not cleaned_data2 or not cleaned_data3 or not cleaned_data4 or not cleaned_data5:
            raise forms.ValidationError("Please fill all the blanks")
        if exist:
            print("email already exists")
            raise forms.ValidationError("Email already registered")
        if cleaned_data2!=cleaned_data3:
            print("passwords do not match")
            self.add_error('password2',cleaned_data2)
            raise forms.ValidationError("Passwords do not match, please try again")
        return cleaned_data


class likes(models.Model):
    likes=forms.FileField()



class favorites(models.Model):
    favorites=forms.FileField()