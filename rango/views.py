from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render

from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm
from rango.forms import UserProfileForm

from rango.models import Category, UserProfile
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

    # request.session.set_test_cookie()
    return render(request, 'rango/index.html', context_dict)


def about(request):
    # if request.session.test_cookie_worked():
        # print('Test cookie worked')
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


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'profile_form': profile_form,
                   'user_form': user_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")

    else:
        return render(request, "rango/login.html")


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
