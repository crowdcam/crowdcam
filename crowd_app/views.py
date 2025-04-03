from django.shortcuts import render
from .models import Media

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



