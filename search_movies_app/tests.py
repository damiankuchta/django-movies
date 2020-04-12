from django.test import TestCase
from . import utils, views
from django.urls import resolve, reverse
from django.test import Client


class UtilsGetMovieGenresTest(TestCase):
    def test_get_genres(self):
        genres = utils.get_movies_genres()
        self.assertIsInstance(genres, list)
        for genre in genres:
            self.assertIsInstance(genre, dict)
            self.assertIsInstance(genre['id'], int)
            self.assertIsInstance(genre['name'], str)

    def test_get_genres_option_field(self):
        genres = utils.get_movies_genres_option_field()
        self.assertIsInstance(genres, list)
        for genre in genres:
            self.assertIsInstance(genre, tuple)
            self.assertIsInstance(genre[0], int)
            self.assertIsInstance(genre[1], str)


class UtilsGetMoviesTest(TestCase):
    def test_succsefull_get_movies_by_genres(self):
        genre_query_parameters = {"with_genres": "12",
                                       "sort_by": "popularity.desc",
                                       "page": "1"}.items()
        total_pages, results = utils.get_moves_by_genres(genre_query_parameters)
        self.assertTrue(total_pages)
        self.assertTrue(results)

    def test_sucesfull_get_movies_by_title(self):
        name_query_parameters = {"query": "Batman",
                                      "page": 1}.items()
        total_pages, results = utils.get_movies_by_title(name_query_parameters)
        self.assertTrue(total_pages)
        self.assertTrue(results)

    def test_unsucesfull_get_movies_by_title(self):
        invalid_name_query_parametest = {}.items()
        total_pages, results = utils.get_movies_by_title(invalid_name_query_parametest)
        self.assertFalse(total_pages)
        self.assertFalse(results)

    def test_sucesfull_get_most_popular_movies(self):
        total_pages, results = utils.get_most_popular_movies()
        self.assertTrue(total_pages)
        self.assertTrue(results)


class FormHandlerViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("search-movies-form-handler")

    def test_redirect(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("search-movies"), target_status_code=200)

    def test_view(self):
        view = resolve(reverse("search-movies-form-handler"))
        self.assertEqual(view.func, views.search_movies_form_handler)

    def test_sucesfull_post_genres(self):
        data = {"with_genres": ["12","16"],
                "sort_by": "popularity.desc"}
        response = self.client.post(self.url, data=data, follow=True)
        last_url, status_code = response.redirect_chain[-1]
        query_parameter = last_url.split("&")
        self.assertEqual("/?search_type=genres", query_parameter[0])
        self.assertEqual("with_genres=12,16", query_parameter[1])
        self.assertEqual("sort_by=popularity.desc", query_parameter[2])

    def test_sucesfull_post_titles(self):
        data = {"query": "Batman"}
        response = self.client.post(self.url, data=data, follow=True)
        last_url, status_code = response.redirect_chain[-1]
        query_parameter = last_url.split("&")
        self.assertEqual("/?search_type=title", query_parameter[0])

    def test_unsucesfull_post(self):
        data = {}
        response = self.client.post(self.url, data=data, follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertEqual("/", last_url)

class SearchMoviesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("search-movies")

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view(self):
        view = resolve(reverse("search-movies"))
        self.assertEqual(view.func, views.search_movies)

    def test_sucesfull_results_genres(self):
        query_param = "?search_type=genres&with_genres=16,12&sort_by=popularity.desc&page=1"
        genres = [16, 12]
        response = self.client.get(self.url + query_param)
        for movie in response.context['movies_list']:
            for genre in genres:
                self.assertIn(genre, movie["genre_ids"])

    def test_sucesfull_results_titles(self):
        query_param = "?search_type=title&query=Batman&page=1"
        response = self.client.get(self.url + query_param)
        for movie in response.context['movies_list']:
           self.assertIn("Batman", movie['title'])

    def test_sucesfull_results_popular(self):
        query_param = ""
        response = self.client.get(self.url + query_param)
        try:
            movies = response.context['movies_list']
        except:
            movies = None
        self.assertTrue(movies)

# class AddToWatchedTest(TestCase):
#     def setUp(self):
#         self.user =
#         self.client = Client()
#         self.client.force_login()
#         self.url = reverse("search-movies_app")
#     #
#     # def test_add_to_watched_function(self):
#     #
#     #     views.add_to_watch_list
