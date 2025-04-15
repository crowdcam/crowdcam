from django.urls import path
from . import views

app_name = "organization"

urlpatterns = [
    path("create_org/", views.create_org, name="create_org"),
    path("<int:org_id>", views.org_view, name="org_view"),
    path("", views.user_orgs, name="user_orgs"),
    path("<int:org_id>/admin", views.admin_index, name="admin_index"),
    path("<int:org_id>/admin/join_code", views.set_join_code, name="set_join_code")
    
]
