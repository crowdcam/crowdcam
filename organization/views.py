from django.shortcuts import render

# Create your views here.
def create_org(request):
    return render(request, "organization/index.html")