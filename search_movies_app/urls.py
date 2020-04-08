from django.urls import path
from . import views

urlpatterns = [
    path('search/form_handler/', views.search_movies_form_handler, name="search-movies-form-handler"),
    path('search/<int:movie_id>/<str:action_to_perform>', views.add_to_watched_wishlisted, name="add-to-watched-wishlist"),
    path('', views.search_movies, name="search-movies"),
]
