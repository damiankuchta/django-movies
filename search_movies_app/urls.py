from django.urls import path
from . import views

urlpatterns = [
    path('search/form_handler/', views.search_movies_form_handler, name="search-movies-form-handler"),
    path('', views.search_movies, name="search-movies"),
]
