from django import forms

class Video(forms.Form):
    title=forms.CharField(max_length=200,required=True)
    description=forms.CharField(max_length=20000,required=True)
    video=forms.FileField(required=True)
