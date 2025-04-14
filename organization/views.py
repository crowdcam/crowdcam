from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Organization
from .forms import OrganizationForm


# login_url redirects users to the provided url given they are not logged in
# @login_required is a decorator that says hey this needs login
@login_required()
def create_org(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            # add data from form
            org = form.save(commit=False)
            org.save()
            # send user to media index page after success
            return redirect('/')
    else:
        form = OrganizationForm()

    return render(request, "organization/create_org.html", {'form': form})