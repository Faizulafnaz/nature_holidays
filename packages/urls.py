from django.urls import path
from . import views

app_name = 'packages'

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.PackageListView.as_view(), name='package_list'),
    path('package/<int:pk>/', views.PackageDetailView.as_view(), name='package_detail'),
    path('search/', views.search_packages, name='search_packages'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
]