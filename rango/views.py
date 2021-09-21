from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from rango.forms import CategoryForm, PageForm
from rango.google_search import run_query
from rango.models import Category, Page


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
    visitor_cookie_handler(request)

    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {
        "my_name": "Aiver",
    }

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context_dict)


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


@login_required
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


@login_required
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


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val

    return val


def search(request):
    context_dict = {}

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            context_dict['query'] = query
            context_dict['result_list'] = run_query(query)

    return render(request, 'rango/search.html', context_dict)
