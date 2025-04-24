from .models import Organization

def get_user_orgs(user):
    orgs = []
    for org in Organization.objects.all():
        if user.has_perm('organization.user', org):
            orgs.append(org)
    return orgs