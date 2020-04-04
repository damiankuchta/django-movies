from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.display_profile, name="display-profile"),
    path('create_user/', views.create_user, name="create-user"),
    path('login/', LoginView.as_view(template_name="user_profiles_app/login_user.html"), name="login-user"),
]
