from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Media, Tag
from organization.models import Organization
from django.http import HttpResponse
from organization.utils import user_has_mod_perms, user_has_user_perms
from .forms import MediaForm, MediaTagForm
import random
import zipfile
import os
import io

# colors for random bg
colors = [
    "#F07857",
    "#43A5BE",
    "#53BDA5",
    "#F5C26B",
    "#253342",
    "#CBD6E2",
    "#4FB06D",
    "#F07857",
    "#EBB8DD",
    "#5C62D6",
    "#BE398D",
    "#D49137",
    "#CAE7D3",
    "#BF2C34",
    "#800080",
]
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
def media_download(request, org_slug):
    org = get_object_or_404(Organization, slug=org_slug)
    user_has_user_perms(request.user, org.id)

    media_list = Media.objects.filter(organization=org).filter(status=True)

    buffer = io.BytesIO()
    
    zip_file_path = f'{org.name}-media.zip'
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip:
    # Add files to the archive here
        for media in media_list:
            zip.write(media.media_path.path, arcname=os.path.basename(media.media_path.name))

    buffer.seek(0)
    response = HttpResponse(
        buffer,
        content_type="application/x-zip-compressed",
        headers={"Content-Disposition": f'attachment; filename={zip_file_path}'},
    )     
    return response  
    

@login_required()
def media_view(request, org_slug, media_id):
    org = get_object_or_404(Organization, slug=org_slug)
    user_has_user_perms(request.user, org.id)

    media = get_object_or_404(Media, id=media_id, organization=org)

    can_delete = request.user.has_perm('mod', org) or media.user == request.user

    if request.method == 'POST':
        form = MediaTagForm(request.POST, organization=org)
        if form.is_valid():
            selected_tags = form.cleaned_data['tags']
            new_tag_name = form.cleaned_data.get('new_tag_name', '').strip()

            if new_tag_name:
                new_tag, created = Tag.objects.get_or_create(
                    name= new_tag_name,
                    organization= org,
                    bg_color= random.choice(colors)
                )
                selected_tags = list(selected_tags)
                selected_tags.append(new_tag)

            media.tag.set(selected_tags)
            return redirect('media_app:media_view', org_slug= org.slug, media_id= media.id)
        
    else:
        form = MediaTagForm(
            initial= {'tags': media.tag.all()},
            organization= org,
        )

    context = {
        "media": media,
        "org": org, 
        'can_delete': can_delete,
        'form': form,
    }
    return render(request, "media_app/view.html", context)


# login_url redirects users to the provided url given they are not logged in
# @login_required is a decorator that says hey this needs login
@login_required()
def upload(request, org_slug):

    org = get_object_or_404(Organization, slug=org_slug)
    user_has_user_perms(request.user, org.id)

    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES, organization=org)
        if form.is_valid():
            files = form.cleaned_data['file_field']
            tags = list(form.cleaned_data.get('tags', []))
            new_tags_name = form.cleaned_data.get('new_tag_name')

            if new_tags_name:
                new_tag = Tag.objects.create (
                    name= new_tags_name,
                    organization= org,
                    bg_color= random.choice(colors)
                )
                tags.append(new_tag)

            for file in files:
                media = Media.objects.create (
                    media_path = file,
                    user = request.user,
                    organization = org,
                )
                media.tag.set(tags)

            media.save()
            # send user to media index page after success
            return redirect(reverse('media_app:media_index', args=[org_slug]))
    else:
        form = MediaForm(organization=org)
    return render(request, "media_app/upload.html", {'form': form, 'org': org})

@login_required()
def delete_media(request, org_slug, media_id):
    org = get_object_or_404(Organization, slug=org_slug)
    user_has_mod_perms(request.user, org.id)
    media = get_object_or_404(Media, id=media_id)

    media.media_path.delete(save=False)  # Delete the file from disk
    media.delete()                      # Delete the record from DB
    return redirect(reverse('media_app:media_index', args=[org_slug]))

@login_required()
def user_media(request, filter=None):
    
    if(filter is None):
        media_list = Media.objects.filter(user=request.user).filter(status=None).order_by("created")
    elif(filter == "approved"):
        media_list = Media.objects.filter(user=request.user).filter(status=True).order_by("created")
    elif(filter == "all"):
        media_list = Media.objects.filter(user=request.user).order_by("created")
    else:
        media_list = Media.objects.filter(user=request.user).filter(status=False).order_by("created")

    context = {"media_list": media_list, "filter": filter}
    return render(request, "media_app/user_media.html", context)

@login_required
def tag_index(request, org_slug):
    org = get_object_or_404(Organization, slug=org_slug)
    user_has_user_perms(request.user, org.id)

    tags = Tag.objects.filter(organization=org).order_by("-name")

    context = {
        "tags": tags,
        "org": org
    }
    return render(request, "media_app/tag_index.html", context)

@login_required()
def tag_view(request, org_slug, tag_id):
    org = get_object_or_404(Organization, slug=org_slug)
    user_has_user_perms(request.user, org.id)

    tag = get_object_or_404(Tag, id= tag_id, organization= org)
    media_list = Media.objects.filter(tag= tag).order_by("-created")

    context = {
        "tag": tag,
        "media_list": media_list,
        "org": org, 
    }
    return render(request, "media_app/tag_view.html", context)

@login_required()
def delete_tag(request, org_slug, tag_id):
    org = get_object_or_404(Organization, slug=org_slug)
    tag = get_object_or_404(Tag, id=tag_id, organization= org)

    tag.delete()                      # Delete the record from DB
    return redirect(reverse('media_app:tag_index', args=[org_slug]))
  