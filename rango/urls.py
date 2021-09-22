from django.urls import path

from rango import views

app_name = 'rango'

urlpatterns = [
    path('about/', views.AboutView.as_view(), name="about"),
    path('', views.IndexView.as_view(), name="index"),
    path('category/<slug:category_name_slug>/',
         views.ShowCategoryView.as_view(), name='show_category'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<slug:category_name_slug>/add_page/',
         views.AddPageView.as_view(), name='add_page'),
    path('restricted/', views.RestrictedView.as_view(), name="restricted"),
    path('logout/', views.UserLogoutView.as_view(), name="logout"),
    #     path('search/', views.search, name="search"),
    path('goto/', views.GoToUrlView.as_view(), name='goto'),
    path('profile/<username>', views.ShowProfileView.as_view(), name='profile'),
    path('profiles/', views.ListProfileView.as_view(), name='list_profiles'),
    path('register_profile/', views.RegisterProfileView.as_view(),
         name='register_profile'),
    path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),
    path('suggest/', views.CategorySuggestionView.as_view(), name='suggest'),
    path('search_add_page/', views.SearchAddPageView.as_view(),
         name='search_add_page')
]
