"""Market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from article.sitemaps import PostSitemap
from article.views import post_list
from django.conf import settings
from django.conf.urls.static import static
from information.views import dashboard
from django.conf.urls.i18n import i18n_patterns

sitemaps = {'posts': PostSitemap, }

urlpatterns = i18n_patterns(
    path('', post_list),
    path('admin/', admin.site.urls),
    path('article/', include('article.urls', namespace='article')),
    path('information/', include('information.urls', namespace='information')),
    path('actions/', include('actions.urls', namespace='actions')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('accounts/profile/', dashboard),
    path('accounts/', include('allauth.urls')),
    path('rosetta/', include('rosetta.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
