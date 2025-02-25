from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.CharField(max_length=50)
    bio = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)