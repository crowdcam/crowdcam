from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import user_has_mod_perms
from media_app.models import Media


@login_required()
def mod_index(request, org_id):
    org = user_has_mod_perms(request.user, org_id)
    context = {"org": org}
    return render(request, "organization/mod/index.html", context)



@login_required()
def review_all(request, org_id):
    org = user_has_mod_perms(request.user, org_id)
    media_list = Media.objects.filter(organization=org).order_by("-created")
    context = {"org": org, "media_list": media_list}
    return render(request, "organization/mod/review.html", context)