from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("create_user/", views.create_user, name="create_user"),
    path("media", views.media_index, name="media_index"),
    path("media/<int:media_id>", views.media_view, name="media_view"),
    path("login/", LoginView.as_view(template_name="crowd_app/login.html"), name='login')
]