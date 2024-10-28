from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from apps.ranking.sitemaps import RankingSitemap, NavLinkSitemap, TeamSitemap
from config.main_views import HomeView, robots_txt, ads_txt

sitemaps = {
    'ranking': RankingSitemap,
    'nav-links': NavLinkSitemap,
    'team-detail': TeamSitemap,
}

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin', admin.site.urls),
    path('', include('apps.ranking.urls')),
    path('', include('apps.team.urls')),
    path('', include('apps.game.urls')),
    path('robots.txt', robots_txt),
    path('ads.txt', ads_txt),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
