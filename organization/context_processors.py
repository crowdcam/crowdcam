from .utils import get_user_orgs

def user_organizations(request):
    if request.user.is_authenticated:
        return {'user_orgs': get_user_orgs(request.user)}
    return {'user_orgs': []}