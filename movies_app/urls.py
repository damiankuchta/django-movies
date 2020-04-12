from django.urls import path
from . import views

urlpatterns = [
    path("<int:movie_id>/", views.display_movie, name="display-movie")
]
