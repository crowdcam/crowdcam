from django.urls import path
from . import views
from media_app import views as media_views
app_name = "crowd_app"

urlpatterns = [
    path("", views.index, name="home"),
    path("mymedia", media_views.user_media, name="user_media"),
    path("mymedia/<str:filter>", media_views.user_media, name="user_media")
]