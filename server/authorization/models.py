from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from rest_framework_simplejwt.tokens import RefreshToken

class User(AbstractUser):
    bio = models.TextField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set', 
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  
        blank=True,
    )
    def tokens(self):
        token = RefreshToken.for_user(self)
        return {
            'access_token': str(token.access_token),
            'refresh_token': str(token),
        }