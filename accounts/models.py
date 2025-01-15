from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_agent = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

    # Allow profile picture to be optional with a default path and a designated upload folder
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg', null=True, blank=True)

    def __str__(self):
        return self.username

