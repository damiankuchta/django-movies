from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from user_profiles_app.models import UserProfile

from movies_project import utils
from movies_project.context_processor_forms import SelectGenreForm, SearchMoviesForm


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

    """ pages quary parameter must stay last, last element from query url will be deleted in "search_movies" to change pages """
    query_params += "page={page}".format(page=page)  if query_params != "?" else ""

    return redirect(reverse("search-movies") + query_params)


def search_movies(request):
    selecet_genre_form = SelectGenreForm(initial={"sort_by": request.GET.get('sort_by')})

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


    user = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else UserProfile()
    watched_movies = list(map(int, user.watched_movies.split())) if user.watched_movies is not None else None
    wishlisted_movies = list(map(int, user.wishlisted_movies.split())) if user.wishlisted_movies is not None else None

    return render(request, "search_movies_app/display_movies.html", {"selecet_genre_form": selecet_genre_form,
                                                                     "list_of_genres_from_query_parameter": list_of_genres_from_query_parameter,
                                                                     "movies_list": movies_list,
                                                                     "pages": pages,
                                                                     "query_parameters_url": query_parameters_url,
                                                                     "watched_movies": watched_movies,
                                                                     "wishlisted_movies": wishlisted_movies})
