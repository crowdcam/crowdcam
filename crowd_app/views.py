from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "crowd_app/index.html")

def error(request, exception):
    context = {"exception": exception}
    print("Exception:" + str(exception))
    return render(request, "crowd_app/error.html", context)
