import requests as tmdb_requests


tmdb_api_key='e37969a8464642a43ea8e9094892b371'
url = "https://api.themoviedb.org/3/"


"""
    Sends get reguest to TMDB to get all the possible genres and their ids
    returns list with tumples
"""
def get_movies_genres():
    genres_url = "genre/movie/list"
    tmdb_response = tmdb_requests.get(url+genres_url, params={"api_key": tmdb_api_key})
    return tmdb_response.json()['genres']


"""
    Same as above, with the difference that this returns genres in optionfield valid format
"""
def get_movies_genres_option_field():
    genres = get_movies_genres()
    genres_options = [(g['id'], g['name']) for g in genres]
    return genres_options


"""
    Receives list of query parameteres
    Sends requests to TMDB qith recived parameters
    Returns Json with movies list and total list of pages
"""
def get_moves_by_genres(query_parameters):
    discover_url = "discover/movie"
    data = {"api_key": tmdb_api_key}
    for key, value in query_parameters:
        data.update({"{}".format(key): value})
    tmdb_response = tmdb_requests.get(url + discover_url, params=data)

    if len(tmdb_response.json()) < 4:
        return 0, []
    return tmdb_response.json()['total_pages'], tmdb_response.json()['results']



"""
    Receives string with move name
    returns json with with total pages and results
"""
def get_movies_by_title(query_parameters):
    search_url = "search/movie"
    data = {"api_key": tmdb_api_key}
    for key, value in query_parameters:
        data.update({"{}".format(key): value})
    tmdb_response = tmdb_requests.get(url + search_url, params=data)

    if len(tmdb_response.json()) < 4:
        return 0, []
    return tmdb_response.json()['total_pages'], tmdb_response.json()['results']


def get_most_popular_movies(page=1):
    search_url = "movie/popular"
    data = {"api_key": tmdb_api_key}
    data.update({"page": page})
    tmdb_response = tmdb_requests.get(url + search_url, params=data)

    if len(tmdb_response.json()) < 4:
        return 0, []
    return tmdb_response.json()['total_pages'], tmdb_response.json()['results']


def get_pages_numbers_to_show(current_page_number, total_pages, pages_on_each_side=4):
    min_page = int(current_page_number) - pages_on_each_side
    max_page = int(current_page_number) + pages_on_each_side
    pages = []
    for r in range(min_page,max_page):
        if r > 0 and r < total_pages:
            pages.append(r)
    return pages