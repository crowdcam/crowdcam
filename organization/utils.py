from .models import Organization
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

def get_user_orgs(user):
    orgs = []
    for org in Organization.objects.all():
        if user.has_perm('organization.user', org):
            orgs.append(org)
    return orgs

def user_has_admin_perms(user, org_id):
    org = get_object_or_404(Organization, id=org_id)
    if(not(user.has_perm('admin', org))):
        raise PermissionDenied()
    return org

def user_has_user_perms(user, org_id):
    org = get_object_or_404(Organization, id=org_id)
    if(not(user.has_perm('user', org))):
        raise PermissionDenied()
    return org