from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import user_has_mod_perms



@login_required()
def mod_index(request, org_id):
    org = user_has_mod_perms(request.user, org_id)
    context = {"org": org}
    return render(request, "organization/mod/index.html", context)