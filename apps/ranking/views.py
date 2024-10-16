from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView

from apps.ranking.models import Team


class RankingView(ListView):
    model = Team
    template_name = 'ranking.html'
    context_object_name = 'teams'

    def get_queryset(self):
        continent = self.request.GET.get('continent')
        if continent:
            return Team.objects.filter(current_rank__isnull=False, confederation=continent)
        return Team.objects.filter(current_rank__isnull=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['continents'] = Team.CONFEDERATION_CHOICES[:-1]
        return context


class CountryListView(ListView, PermissionRequiredMixin):
    model = Team
    template_name = 'country_list.html'
    context_object_name = 'teams'

    def get_queryset(self):
        return Team.objects.order('name')
