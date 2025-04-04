from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register_user(request):
    if(request.method == "POST"):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            # redirect to app_name:page_in_app
            return redirect("/media")
    else: 
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "users/register.html", context)