"""artalk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
# urls.py配置如下，for media访问
from django.conf.urls import url
from django.views.static import serve
from .settings import MEDIA_ROOT
urlpatterns = [
    path('Ryaninnerpeace/admin/', admin.site.urls),
    path('', include('artalk_base.urls')),           #2
    #path('', RedirectView.as_view(url='/artalk/', permanent=True)),
    #path('accounts/', include('django.contrib.auth.urls')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #4

