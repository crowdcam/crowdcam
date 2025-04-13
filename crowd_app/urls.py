from django.urls import path
from . import views

app_name = "crowd_app"

urlpatterns = [
    path("", views.index, name="home"),
    path("media", views.media_index, name="media_index"),
    path('media/delete/<int:media_id>', views.delete_media, name='media_delete'),
    path("media/<int:media_id>", views.media_view, name="media_view"),
    path("upload/", views.upload, name="upload"),
]