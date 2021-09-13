from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    context_dict = {
        "bold_message": "Cupcake",
    }

    return render(request, 'rango/index.html', context=context_dict)
    # return HttpResponse("Rango says hey")


def about(request):
    print(request)
    return HttpResponse("Rango says here is the about page")
