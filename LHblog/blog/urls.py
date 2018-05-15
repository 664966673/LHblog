"""LHblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.urls import include
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name='blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name = "index"),
    re_path(r'^article/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name = "detail"),
    re_path(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name = "category"),
    re_path(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchiveView.as_view(), name = "archive"),
    #path('login/', views.login, name = "login")
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
