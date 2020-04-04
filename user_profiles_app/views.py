from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from search_movies_app.forms import SearchMoviesForm
from .models import UserProfile

# Create your views here.
def display_profile(request):
    pass

def create_user(request):
    search_movie_form = SearchMoviesForm()

    if request.POST:
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            UserProfile(user=user).save()
    else:
        user_creation_form = UserCreationForm()
    return render(request, "user_profiles_app/create_new_user.html", { "user_creation_form": user_creation_form,
                                                                       "search_movie_form": search_movie_form})


#todo mark as watched
#todo add to watchlist

#todo profile = watched
#todo profile - watchlist