from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path("create_user/", views.register_user, name="create_user"),
]