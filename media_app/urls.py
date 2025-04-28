from django.urls import path
from . import views

app_name = "media_app"

urlpatterns = [
    path("", views.media_index, name="media_index"),
    path('delete/<int:media_id>', views.delete_media, name='media_delete'),
    path("<int:media_id>", views.media_view, name="media_view"),
    path("upload/", views.upload, name="upload")
]