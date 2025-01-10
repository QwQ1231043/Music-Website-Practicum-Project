from django import forms
from .models import *
class ManagementFolderForm(forms.ModelForm):
    class Meta:
        model=management_folders
        fields=['title']
class Video(forms.Form):
    title=forms.CharField(max_length=200,required=True)
    description=forms.CharField(max_length=20000,required=True)
    video=forms.FileField(required=True)
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class changed_data(forms.Form):
    username=forms.CharField(max_length=120,required=False)
    age = forms.IntegerField(required=False)
    introduction = forms.CharField(max_length=500,required=False)
    avatar = forms.ImageField(required=False)
