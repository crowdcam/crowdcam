from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
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

def create_user(request):
    form = None

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            form.save()  # Save the new user to the database
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')  # Redirect to the login page or another page
        else:
            messages.error(request, form.errors)
        
    else:
        form = UserCreationForm()
        
    context = {"form": form}
    return render(request, 'crowd_app/create_user.html', context)

