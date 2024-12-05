from django.db import models

# Create your models here.
class emailVerification(models.Model):
    email = models.EmailField()
    verfication_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
