from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

app_name = "users"

# Create your views here.
def register_user(request):
    if(request.method == "POST"):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            # redirect to app_name:name_of_page
            return redirect("crowd_app:media_index")
    else: 
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "users/register.html", context)