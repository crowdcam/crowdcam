from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = "users"

urlpatterns = [
    path("create_user/", views.register_user, name="create_user"),
    path("login/", views.user_login, name="login"),
    
]