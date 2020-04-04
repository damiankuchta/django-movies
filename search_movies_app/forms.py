from django import forms
from .utils import get_movies_genres_option_field


class SelectGenreForm(forms.Form):
    sorting_options = [("popularity.desc", "Popularity down"),
                       ("popularity.asc", "Popularity up"),
                       ("release_date.asc,", "Relase date up"),
                       ("release_date.desc,", "Relase date down"),
                       ("original_title.asc,", "Title up"),
                       ("original_title.desc,", "Title Down"),
                       ("vote_average.asc,", "Avarage votes up"),
                       ("vote_average.desc,", "Avarage votes down"),
                       ("vote_count.asc,", "Vote cuont up"),
                       ("vote_count.desc", "Vote count down")]
    genre_options = get_movies_genres_option_field()

    with_genres = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                            choices=genre_options)
    sort_by = forms.ChoiceField(choices=sorting_options)


class SearchMoviesForm(forms.Form):
    query = forms.CharField(max_length=124, required=False)