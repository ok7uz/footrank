from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from apps.ranking.sitemaps import RankingSitemap, NavLinkSitemap


class HomeView(RedirectView):
    url = reverse_lazy('ranking')


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


def robots_txt(request):
    lines = [
        'User-Agent: *',
        'Disallow: /admin/',
        'Allow: /\n',
        'Sitemap: https://rankfoot.com/sitemap.xml'
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


sitemaps = {
    'ranking': RankingSitemap,
    'nav-links': NavLinkSitemap,
}

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin', admin.site.urls),
    path('', include('apps.ranking.urls')),
    path('robots.txt', robots_txt),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
