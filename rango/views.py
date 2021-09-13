from django.db import close_old_connections
from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category
from rango.models import Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {
        'bold_message': 'Cruncy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
    }

    try:
        top_five_pages = Page.objects.order_by('-views')[:5]
        print('top_five_pages', top_five_pages)
        context_dict['top_five_pages'] = top_five_pages
    except Page.DoesNotExist:
        context_dict['top_five_pages'] = None

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
