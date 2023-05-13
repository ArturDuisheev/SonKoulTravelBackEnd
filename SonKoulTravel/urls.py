"""SonKoulTravel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from SonKoulTravel import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_page/', include('main_page.urls')),
    path('actions/', include('client_actions.urls')),
    path('tour/', include('tour.urls')),
    path('blog/', include('blog_and_news.urls')),
    path('car/', include('transport.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
