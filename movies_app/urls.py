from django.urls import path
from . import views

urlpatterns = [
    path("<int:movie_id>/", views.display_movie, name="display-movie"),
    path("<int:movie_id>/add_comment_form_handler/", views.add_comment_form_handler, name="add_comment_form_handler"),
    path("<int:movie_id>/add_review_form_handler/", views.add_review_form_handler, name="add_review_form_handler"),
]
