from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Media, Organization
from .forms import MediaForm


# Create your views here.
def index(request):
    return render(request, "crowd_app/index.html")


def media_index(request):
    media_list = Media.objects.order_by("-created")
    context = {"media_list": media_list}
    return render(request, "crowd_app/media/index.html", context)


def media_view(request, media_id):
    media = Media.objects.get(id=media_id)
    context = {"media": media}
    return render(request, "crowd_app/media/view.html", context)


# login_url redirects users to the provided url given they are not logged in
# @login_required is a decorator that says hey this needs login
@login_required()
def upload(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            # add data from form
            media = form.save(commit=False)
            # add user data
            media.user = request.user
            # set organization from user data
            # media.organization = request.user.organization
            #TODO Properly set organization once properly added
            media.organization = Organization.objects.first() # had to do this since users don't have organization right now

            media.save()
            # send user to media index page after success
            return redirect('/media')
    else:
        form = MediaForm()

    return render(request, "crowd_app/media/upload.html", {'form': form})

def delete_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)

    media.media_path.delete(save=False)  # Delete the file from disk
    media.delete()                      # Delete the record from DB
    return redirect('/media')
