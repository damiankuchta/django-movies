from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.display_profile, name="display-profile"),
    path('create_user/', views.create_user, name="create-user"),
    path('login/', LoginView.as_view(template_name="user_profiles_app/login_user.html"), name="login-user"),
    path('logout/', views.logout_user, name="logout-user"),
    path('watched_wishlist_form_hander/', views.watched_wishlist_form_hander, name="watched_wishlist_form_hander"),
    path('<str:watched_or_wishlisted>/<int:page_to_display>/', views.watched_whslist, name="watched_or_wishlisted"),

    path('<int:movie_id>/<str:action_to_perform>/', views.add_to_watched_wishlisted,
         name="add-to-watched-wishlist"),


]
