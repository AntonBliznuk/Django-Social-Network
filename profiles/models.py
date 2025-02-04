from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from decouple import config


"""
Custom user model for storing image.
"""
class CustomUser(AbstractUser):
    profile_picture = CloudinaryField('image', default=config('DEFAULT_USER_PHOTO_URL'))

    def __str__(self) -> str:
        return f"{self.username} -> {self.id}"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username', '-date_joined']


"""
A model for storing user subscriptions to other users.
"""
class Subscribe(models.Model):
    user_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False, related_name='Subscribe_from')
    user_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False, related_name='Subscribe_to')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user_from} --> {self.user_to}({self.date})"
    
    class Meta:
        verbose_name = 'Subscribe'
        verbose_name_plural = 'Subscribes'
        ordering = ['-date']