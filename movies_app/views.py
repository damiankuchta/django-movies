from django.shortcuts import render, redirect
from movies_project.utils import get_movies_by_id
from . import forms
from . import models
from django.contrib.auth.decorators import login_required

# Create your views here.
def display_movie(request, movie_id):
    comment_form = forms.AddComment()
    review_form = forms.AddReview()
    movie = get_movies_by_id(str(movie_id))
    comments = models.Comments.objects.filter(movie_id=movie['id']).all()

    watched_or_wishlisted = None
    if request.user.is_authenticated:
        if str(movie_id) in str(request.user.profile.values('wishlisted_movies')[0]['wishlisted_movies']).split():
            watched_or_wishlisted = "wishlisted"
        elif str(movie_id) in str(request.user.profile.values('watched_movies')[0]['watched_movies']).split():
            watched_or_wishlisted = "watched"

    return render(request, "movies_app/movie.html", {"movie": movie,
                                                     "comment_form": comment_form,
                                                     "review_form": review_form,
                                                     "comments": comments,
                                                     "watched_or_wishlisted": watched_or_wishlisted})


@login_required
def add_comment_form_handler(request, movie_id):

    new_comment = models.Comments(user=request.user, movie_id=movie_id)
    comment_form = forms.AddComment(request.POST, instance=new_comment)
    if comment_form.is_valid():
        comment_form.save()
    return redirect("display-movie", movie_id=movie_id)


@login_required
def add_review_form_handler(request, movie_id):
    if request.POST:
        new_review = models.Reviews(user=request.user)
        review_form = forms.AddReview(request.POST, instance=new_review)
        if review_form.is_valid():
           review_form.save()
    return redirect("display-movie", movie_id=movie_id)