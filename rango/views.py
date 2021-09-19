from rango.forms import CategoryForm
from rango.forms import PageForm
from django.db import close_old_connections
from django.shortcuts import redirect
from django.urls import reverse
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
            # "MEDIA_URL": "/media/cat.jpg"
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


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return redirect('/rango/')

    form = PageForm()
    if (request.method == 'POST'):
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)
