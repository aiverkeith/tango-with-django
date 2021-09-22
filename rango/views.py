from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from rango.forms import CategoryForm, PageForm, UserProfileForm
from rango.google_search import run_query
from rango.models import Category, Page, UserProfile


class IndexView(View):
    def get(self, request):
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


class AboutView(View):
    def get(self, request):
        context_dict = {}
        context_dict['visits'] = request.session['visits']

        return render(request, 'rango/about.html', context_dict)


class ShowCategoryView(View):
    def get(self, request, category_name_slug):
        context_dict = {}

        try:
            category = Category.objects.get(slug=category_name_slug)
            pages = Page.objects.filter(category=category).order_by('-views')
            context_dict['pages'] = pages
            context_dict['category'] = category
        except Category.DoesNotExist:
            context_dict['pages'] = None
            context_dict['category'] = None

        return render(request, 'rango/category.html', context_dict)

    def post(self, request, category_name_slug):
        context_dict = {}
        if request.method == 'POST':
            query = request.POST['query'].strip()
            if query:
                context_dict['result_list'] = run_query(query)
                context_dict['query'] = query
        return render(request, 'rango/category.html', context_dict)


class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm
        return render(request, 'rango/add_category.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

        return render(request, 'rango/add_category.html', {'form': form})


class AddPageView(View):
    def get_category(self, category_name_slug):
        try:
            category = Category.objects.get(slug=category_name_slug)
            return category
        except Category.DoesNotExist:
            return None

    @method_decorator(login_required)
    def get(self, request, category_name_slug):
        category = self.get_category(category_name_slug)

        if category is None:
            return redirect(reverse('rango:index'))

        context_dict = {'category': category, 'form': PageForm()}
        return render(request, 'rango/add_page.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, category_name_slug):
        category = self.get_category(category_name_slug)

        if category is None:
            return redirect(reverse('rango:index'))

        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(
                    reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

        return render(request, 'rango/add_page.html', {'category': category, 'form': form})


class RestrictedView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'rango/restricted.html')


class UserLogoutView(View):
    @method_decorator(login_required)
    def get(request):
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


def old_search(request):
    context_dict = {}

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            context_dict['query'] = query
            context_dict['result_list'] = run_query(query)

    return render(request, 'rango/search.html', context_dict)


class GoToUrlView(View):
    def get(self, request):
        page_id = request.GET.get(
            'page_id') if request.method == 'GET' else None

        if page_id:
            try:
                page = Page.objects.get(id=page_id)
                page.views += 1
                page.save()
                return redirect(page.url)
            except Page.DoesNotExist:
                pass
        return redirect(reverse('rango:index'))


class RegisterProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        context_dict = {'form': UserProfileForm()}
        return render(request, 'rango/profile_registration.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('rango:index')
        else:
            print(form.errors)

        context_dict = {'form': form}
        return render(request, 'rango/profile_registration.html', context_dict)


class ShowProfileView(View):
    def get_user_details(self, username):
        user = None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website,
                                'picture': user_profile.picture})
        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect('rango:index')

        context_dict = {
            'userprofile': user_profile,
            'selecteduser': user,
            'form': form,
        }

        return render(request, 'rango/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect('rango:index')

        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)

        context_dict = {'userprofile': user_profile,
                        'selecteduser': user, 'form': form}

        return render(request, 'rango/profile.html', context_dict)


class ListProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()
        print(profiles[0])
        return render(request,
                      'rango/list_profiles.html',
                      {'userprofile_list': profiles})
