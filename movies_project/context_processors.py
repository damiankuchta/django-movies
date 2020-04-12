from .context_processor_forms import SearchMoviesForm, SelectGenreForm

def search_form(request):
    return { 'search_movie_form': SearchMoviesForm() }

