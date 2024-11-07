from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime



User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile_picture.png')
    location = models.CharField(max_length=100, blank=True)
    

    def __str__(self):
        return self.user.username
    