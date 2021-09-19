from django.db import close_old_connections
from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category
from rango.models import Page


def index(request):
    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
    }

    try:
        categories = Category.objects.order_by('-views')[:5]
        context_dict['categories'] = categories
    except Page.DoesNotExist:
        context_dict['categories'] = None

    try:
        pages = Page.objects.order_by('-views')[:5]
        context_dict['pages'] = pages
    except Page.DoesNotExist:
        context_dict['pages'] = None

    return render(request, 'rango/index.html', context_dict)
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


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context_dict)
