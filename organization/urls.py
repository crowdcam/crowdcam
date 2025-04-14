from django.urls import path
from . import views

app_name = "organization"

urlpatterns = [
    path("create_org/", views.create_org, name="create_org"),
]
