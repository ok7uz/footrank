from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.urls import reverse_lazy

from apps.ranking.models import Team


class RankingSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return [None] + Team.CONFEDERATION_CHOICES[:-1]

    def location(self, item):
        if item:
            return reverse_lazy('conf-ranking', kwargs={'conf': item[0]})
        return reverse_lazy('ranking')

    @staticmethod
    def lastmod(obj):
        return datetime.today()


class NavLinkSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['competition_list', 'game_list', 'country_list']

    def location(self, item):
        return reverse_lazy(item)

    @staticmethod
    def lastmod(obj):
        today = datetime.today()
        return datetime(year=today.year, month=today.month, day=1)
