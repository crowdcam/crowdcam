from django.urls import path
from . import views
from . import views_admin

app_name = "organization"

urlpatterns = [
    path("create_org/", views.create_org, name="create_org"),
    path("join_org/", views.join_org, name="join_org"),
    path("<int:org_id>", views.org_view, name="org_view"),
    path("", views.user_orgs, name="user_orgs"),
    path("<int:org_id>/admin", views_admin.admin_index, name="admin_index"),
    path("<int:org_id>/admin/download", views_admin.download_users, name="download_users"),
    path("<int:org_id>/admin/users", views_admin.manage_users, name="manage_users"),
    path("<int:org_id>/admin/users/<int:user_id>", views_admin.manage_user, name="manage_user"),
    path("<int:org_id>/admin/join_code", views_admin.set_join_code, name="set_join_code")
    
    
]
