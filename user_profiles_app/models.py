from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    wishlisted_movies = models.TextField(null=True)
    watched_movies = models.TextField(null=True )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
