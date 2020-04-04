from django.shortcuts import render, redirect, reverse
from . import utils
from .forms import SelectGenreForm, SearchMoviesForm


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


    """
        pages quary parameter must stay last
    """
    if query_params != "?":
        query_params += "page={page}".format(page=page)
    else:
        query_params = ""

    return redirect(reverse("search-movies") + query_params)


def search_movies(request):


    selecet_genre_form = SelectGenreForm(initial={"sort_by": request.GET.get('sort_by')})
    search_movie_form = SearchMoviesForm()

    pages = None
    list_of_genres_from_query_parameter = None

    if request.GET.get('search_type') == "genres":
        total_pages, movies_list = utils.get_moves_by_genres(request.GET.items())
        list_of_genres_from_query_parameter = list(map(int, request.GET.get('with_genres').split(",")))
    elif request.GET.get('search_type') == "title":
        total_pages, movies_list = utils.get_movies_by_title(request.GET.items())
    else:
        total_pages, movies_list = utils.get_most_popular_movies(page=request.GET.get('page'))

    query_parameters_url = request.GET.urlencode().split("&")
    query_parameters_url.pop()
    query_parameters_url = "&".join(query_parameters_url)
    query_parameters_url =None

    if request.GET.get('page'):
        if movies_list:
            pages = utils.get_pages_numbers_to_show(request.GET.get('page'), total_pages)
    else:
        if movies_list:
            pages = utils.get_pages_numbers_to_show(1, total_pages)

    return render(request, "search_movies_app/display_movies.html", {"selecet_genre_form": selecet_genre_form,
                                                                     "search_movie_form": search_movie_form,
                                                                     "list_of_genres_from_query_parameter": list_of_genres_from_query_parameter,
                                                                     "movies_list": movies_list,
                                                                     "pages": pages,
                                                                     "query_parameters_url": query_parameters_url})




