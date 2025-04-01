from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("media", views.media_index, name="media_index"),
    path("media/<int:media_id>", views.media_view, name="media_view")
    
]