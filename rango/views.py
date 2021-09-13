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
    return render(
        request,
        'rango/about.html',
        context={
            "my_name": "Aiver",
            "MEDIA_URL": "/media/cat.jpg"
        }
    )
    # return HttpResponse("Rango says here is the about page")
