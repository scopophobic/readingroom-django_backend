from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.auth.models from User


# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)