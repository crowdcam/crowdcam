from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Media
from organization.models import Organization
from organization.utils import user_has_mod_perms, user_has_user_perms
from .forms import MediaForm

# Create your views here.
@login_required()
def media_index(request, org_slug):
    org = get_object_or_404(Organization, slug=org_slug)
    user_has_user_perms(request.user, org.id)
    
    # Filter media to this organization only
    media_list = Media.objects.filter(organization=org).filter(status=True).order_by("-created")
    
    context = {
        "media_list": media_list,
        "org": org
    }
    return render(request, "media_app/index.html", context)

@login_required()
def media_view(request, org_slug, media_id):
    org = get_object_or_404(Organization, slug=org_slug)
    user_has_user_perms(request.user, org.id)

    media = get_object_or_404(Media, id=media_id, organization=org)

    can_delete = request.user.has_perm('mod', org) or media.user == request.user
    context = {
        "media": media,
        "org": org, 
        'can_delete': can_delete
    }
    return render(request, "media_app/view.html", context)


# login_url redirects users to the provided url given they are not logged in
# @login_required is a decorator that says hey this needs login
@login_required()
def upload(request, org_slug):

    org = get_object_or_404(Organization, slug=org_slug)
    user_has_user_perms(request.user, org.id)

    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data['file_field']

            print(f"Received {len(files)} file(s):", files)

            for file in files:
                print(f"Saving file: {file.name}")
                media = Media.objects.create (
                    media_path = file,
                    user = request.user,
                    organization = org,
                    tag = None,
                )

            media.save()
            # send user to media index page after success
            return redirect(reverse('media_app:media_index', args=[org_slug]))
    else:
        form = MediaForm()
    return render(request, "media_app/upload.html", {'form': form, 'org': org})

@login_required()
def delete_media(request, org_slug, media_id):
    org = get_object_or_404(Organization, slug=org_slug)
    user_has_mod_perms(request.user, org.id)
    media = get_object_or_404(Media, id=media_id)

    media.media_path.delete(save=False)  # Delete the file from disk
    media.delete()                      # Delete the record from DB
    return redirect(reverse('media_app:media_index', args=[org_slug]))