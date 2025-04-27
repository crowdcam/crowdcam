from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils import user_has_mod_perms
from media_app.models import Media
from media_app.forms import MediaReview

@login_required()
def mod_index(request, org_id):
    org = user_has_mod_perms(request.user, org_id)
    context = {"org": org}
    return render(request, "organization/mod/index.html", context)



@login_required()
def review_all(request, org_id, filter=None):
    org = user_has_mod_perms(request.user, org_id)

    if(filter is None):
        media_list = Media.objects.filter(organization=org).filter(status=None).order_by("-created")
    elif(filter == "approved"):
        media_list = Media.objects.filter(organization=org).filter(status=True).order_by("-created")
    elif(filter == "all"):
        media_list = Media.objects.filter(organization=org).order_by("-created")
    else:
        media_list = Media.objects.filter(organization=org).filter(status=False).order_by("-created")
        
    media_forms = []

    for media in media_list:
        form = MediaReview(instance=media)
        media_forms.append({"media": media, "form": form})

    context = {"org": org, "media_forms": media_forms}
    return render(request, "organization/mod/review.html", context)

@login_required()
def media_view_change(request, org_id, media_id):
    user_has_mod_perms(request.user, org_id)
    media = get_object_or_404(Media, id=media_id)

    if request.method == 'POST':
        form = MediaReview(request.POST, instance=media)
        if form.is_valid():
            form.save()
            return redirect('organization:media_review', org_id = org_id)