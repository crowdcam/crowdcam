from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

app_name = "users"


# Create your views here.
def register_user(request):
    if(request.method == "POST"):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):

            # save the user and get the new created user
            new_user = form.save()

            # login as new user
            login(request, new_user)
            
            # redirect to app_name:name_of_page
            return redirect("crowd_app:media_index")
        
    else: 
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "users/register.html", context)


def user_login(request):
    
    if(request.method == "POST"):
        form = AuthenticationForm(data=request.POST)
        if(form.is_valid()):
            login(request, form.get_user())
            return redirect("crowd_app:media_index")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "users/login.html", context)


def user_logout(request):
    if(request.method == "POST"):
        logout(request)
        return redirect("users:login")
    return render(request, "users/logout.html")
