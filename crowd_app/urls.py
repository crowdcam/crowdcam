from django.urls import path
from . import views

app_name = "crowd_app"

urlpatterns = [
    path("", views.index, name="home"),
    path("media", views.media_index, name="media_index"),
    path("media/<int:media_id>", views.media_view, name="media_view"),
]
