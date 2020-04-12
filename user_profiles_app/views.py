from django.shortcuts import render, redirect, reverse

from movies_project.utils import get_movies_by_id, get_pages_numbers_to_show
from movies_project.context_processor_forms import SearchMoviesForm, SelectGenreForm
from .models import UserProfile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login

from django.core.paginator import  Paginator

# Create your views here.

@login_required
def display_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    watched_list = [get_movies_by_id(movie_id) for movie_id in user_profile.watched_movies.split()[:11]]  if user_profile.watched_movies else []
    wishlisted_list = [get_movies_by_id(movie_id) for movie_id in user_profile.wishlisted_movies.split()[:11]]  if user_profile.wishlisted_movies else []

    return render(request, "user_profiles_app/display_profile.html", {"user_profile": user_profile,
                                                                      "wishlisted_movies": wishlisted_list,
                                                                      "watched_movies": watched_list})

def create_user(request):
    search_movie_form = SearchMoviesForm()

    if request.POST:
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            UserProfile(user=user).save()
            login(user)
            return redirect("search-movies")
    else:
        user_creation_form = UserCreationForm()
    return render(request, "user_profiles_app/create_new_user.html", { "user_creation_form": user_creation_form,
                                                                       "search_movie_form": search_movie_form})

@login_required()
def logout_user(request):
    logout(request)
    return redirect("search-movies")


@login_required()
def watched_whslist(request, watched_or_wishlisted, page_to_display=1):

    selecet_genre_form = SelectGenreForm(initial={"sort_by": request.GET.get('sort_by')})

    user_profile = UserProfile.objects.get(user=request.user)

    if watched_or_wishlisted == "watched":
        watched_or_wishlisted_movies = [get_movies_by_id(movie_id) for movie_id in user_profile.watched_movies.split()] if user_profile.watched_movies else []
    elif watched_or_wishlisted == "wishlisted":
        watched_or_wishlisted_movies = [get_movies_by_id(movie_id) for movie_id in user_profile.wishlisted_movies.split()] if user_profile.wishlisted_movies else []
    else:
        redirect("display-profile")

    """ check for genres in movies watched_or_wishlisted_movies, checks whether movie contains 
    all of the genres selected by user """
    movies_list = []

    if request.GET.get("with_genres"):
        list_of_genres_from_query_parameter = list(map(int, request.GET.get('with_genres').split(",")))
        for m in watched_or_wishlisted_movies:
            can_append = 0
            for genre in list_of_genres_from_query_parameter:
                if genre in [genre['id'] for genre in m['genres']]:
                    can_append += 1
                    if can_append == len(list_of_genres_from_query_parameter):
                        movies_list.append(m)
                        continue
    else:
        movies_list = watched_or_wishlisted_movies
        list_of_genres_from_query_parameter = []

    if request.GET.get("sort_by"):
        sort_option = request.GET.get("sort_by").split(".")
        rev = True if sort_option[1] == "desc" else False
        movies_list = sorted(movies_list, key=lambda k: k[sort_option[0]], reverse=rev)


    pages = Paginator(movies_list, 10)
    page = pages.page(page_to_display)
    amount_of_pages = get_pages_numbers_to_show(page_to_display, pages.num_pages+1)

    return render(request, "user_profiles_app/watched_wishlisted.html", {"movies_list": page,
                                                                         "watched_or_wishlisted": watched_or_wishlisted,
                                                                         "amount_of_pages": amount_of_pages,
                                                                         "selecet_genre_form": selecet_genre_form,
                                                                         "list_of_genres_from_query_parameter": list_of_genres_from_query_parameter})


def watched_wishlist_form_hander(request):
    watched_or_wishlisted = request.GET.get('watched_or_wishlisted')
    if request.method == "POST":
        selecet_genre_form = SelectGenreForm(request.POST)
        if selecet_genre_form.is_valid():
            query_params = "?"
            for field in selecet_genre_form:
                if field.name == "with_genres":
                    value = ",".join(field.value())
                else:
                    value = field.value()
                query_params += "{field_name}={field_value}&".format(field_name=field.name, field_value=value)
            return redirect(reverse("watched_or_wishlisted", kwargs={"watched_or_wishlisted": watched_or_wishlisted, "page_to_display": 1}) + query_params)

    return redirect("watched_or_wishlisted", watched_or_wishlisted=watched_or_wishlisted, page_to_display= 1)
#
