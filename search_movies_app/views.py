from django.shortcuts import render, redirect, reverse
from . import utils
from .forms import SelectGenreForm, SearchMoviesForm
from django.contrib.auth.decorators import login_required
from user_profiles_app.models import UserProfile


def search_movies_form_handler(request, page=1):
    query_params = "?"

    if request.method == "POST":
        selecet_genre_form = SelectGenreForm(request.POST)
        search_movie_form = SearchMoviesForm(request.POST)
        if selecet_genre_form.is_valid():
            query_params += "search_type=genres&"
            for field in selecet_genre_form:
                if field.name == "with_genres":
                    value = ",".join(field.value())
                else:
                    value = field.value()
                query_params += "{field_name}={field_value}&".format(field_name=field.name, field_value=value)
        elif search_movie_form.is_valid() and search_movie_form.cleaned_data['query']:
            query_params += "search_type=title&"
            query_params += "query={movie_name}&".format(movie_name=search_movie_form.cleaned_data['query'])

    """ pages quary parameter must stay last """
    if query_params != "?":
        query_params += "page={page}".format(page=page)
    else:
        query_params = ""

    return redirect(reverse("search-movies") + query_params)


def search_movies(request):
    selecet_genre_form = SelectGenreForm(initial={"sort_by": request.GET.get('sort_by')})
    search_movie_form = SearchMoviesForm()

    list_of_genres_from_query_parameter = None

    if request.GET.get('search_type') == "genres":
        total_pages, movies_list = utils.get_moves_by_genres(request.GET.items())
        list_of_genres_from_query_parameter = list(map(int, request.GET.get('with_genres').split(",")))
    elif request.GET.get('search_type') == "title":
        total_pages, movies_list = utils.get_movies_by_title(request.GET.items())
    else:
        total_pages, movies_list = utils.get_most_popular_movies(page=request.GET.get('page'))

    """Deletes last parameter (which should alwasy pe 'page' to make a space for new 'page parameter"""
    query_parameters_url = request.GET.urlencode().split("&")
    query_parameters_url.pop()
    query_parameters_url = "&".join(query_parameters_url)

    if request.GET.get('page'):
        pages = utils.get_pages_numbers_to_show(request.GET.get('page'), total_pages) if movies_list else None
    else:
        pages = utils.get_pages_numbers_to_show(1, total_pages) if movies_list else None

    user = UserProfile.objects.get(user=request.user)

    watched_movies = list(map(int, user.watched_movies.split())) if user.watched_movies is not None else None
    wishlisted_movies = list(map(int, user.wishlisted_movies.split())) if user.wishlisted_movie is not None else None

    return render(request, "search_movies_app/display_movies.html", {"selecet_genre_form": selecet_genre_form,
                                                                     "search_movie_form": search_movie_form,
                                                                     "list_of_genres_from_query_parameter": list_of_genres_from_query_parameter,
                                                                     "movies_list": movies_list,
                                                                     "pages": pages,
                                                                     "query_parameters_url": query_parameters_url,
                                                                     "watched_movies": watched_movies,
                                                                     "wishlisted_movies": wishlisted_movies})


"""
    One function to process two actions, this could be made much simpler with two view functions but I wanted to
    try and squeeze it into one function
"""
@login_required
def add_to_watched_wishlisted(request, movie_id, action_to_perform):
    query_parameters_url = "?" + request.GET.urlencode()
    if action_to_perform == "add_to_watched" or action_to_perform == "add_to_wishlisted":
        user = UserProfile.objects.get(user=request.user)

        watched_movies = list(map(int, user.watched_movies.split())) if user.watched_movies else []
        wishlisted_movies = list(map(int, user.wishlisted_movies.split())) if user.wishlisted_movies else []

        watched_or_wishlisted = watched_movies if action_to_perform == "add_to_watched" else wishlisted_movies
        watched_or_wishlisted_second = wishlisted_movies if action_to_perform == "add_to_watched" else watched_movies

        # DESELECT - SWAP - ADD
        if movie_id in watched_or_wishlisted:  # DeSelect
            watched_or_wishlisted.remove(movie_id)
        elif movie_id in watched_or_wishlisted_second:  # SWap
            watched_or_wishlisted_second.remove(movie_id)
            watched_or_wishlisted.append(movie_id)
        else:  # ADD
            watched_or_wishlisted.append(movie_id)

        watched_or_wishlisted = " ".join(str(s) for s in watched_or_wishlisted) if watched_or_wishlisted else None
        watched_or_wishlisted_second = " ".join(
            str(s) for s in watched_or_wishlisted_second) if watched_or_wishlisted_second else None

        user.watched_movies = watched_or_wishlisted if action_to_perform == "add_to_watched" else watched_or_wishlisted_second
        user.wishlisted_movies = watched_or_wishlisted_second if action_to_perform == "add_to_watched" else watched_or_wishlisted

        user.save()

    return redirect(reverse("search-movies") + query_parameters_url)
