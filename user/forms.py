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
