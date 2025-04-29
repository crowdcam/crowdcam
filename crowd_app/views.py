from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from media_app.models import Media
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "crowd_app/index.html")

def error(request, exception):
    context = {"exception": exception}
    return render(request, "crowd_app/error.html", context)

def media_index(request):
    return HttpResponse("<h1>Fake Media Index Page</h1>")

def media_view(request, media_id):
    return HttpResponse("<h1>Media Detail Page Placeholder - media/testfile.jpg</h1>")

def upload_media(request):
    if request.method == "POST":
        return HttpResponse("Uploaded successfully!")
    return HttpResponse("<h1>Fake Upload Page</h1>")