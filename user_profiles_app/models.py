from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    wishlisted_movies = models.TextField()
    watched_movies = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
