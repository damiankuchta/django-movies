from django.db import models
from django.contrib.auth.models import User


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="comments", null=True)
    movie_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    comment_content = models.CharField(max_length=514)


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="reviews", null=True)
    movie_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    review_content = models.TextField()
