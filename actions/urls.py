"""actions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.urls import include
from instruments import urls as intruments_urls
from util import urls 
from geral import urls as home_urls

from historicos.views import custom_history

from django.conf import settings
from django.conf.urls.static import static

from django.shortcuts import render, redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include(intruments_urls)),
    path('', include(home_urls)),
    path('history/', custom_history, name='my_history'),
    path('ajax/', include(urls),  name='ajax'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
