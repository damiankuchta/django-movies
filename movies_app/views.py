from django.shortcuts import render
from movies_project.utils import get_movies_by_id

# Create your views here.
def display_movie(request, movie_id):
    movie = get_movies_by_id(str(movie_id))
    return render(request, "movies_app/movie.html", {"movie": movie})