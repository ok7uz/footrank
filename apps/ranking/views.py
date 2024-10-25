from datetime import datetime

from django.db.models import F
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView

from apps.ranking.models import Team, Ranking, Period


class RankingView(ListView):
    model = Ranking
    template_name = 'ranking.html'
    context_object_name = 'rankings'
    paginate_by = 100

    def get_queryset(self):
        period_id = self.request.GET.get('period', None)
        today = datetime.today()

        period = get_object_or_404(Period, id=period_id) if period_id else None
        if not period:
            period = Period.objects.filter(start_date__lte=today, end_date__gte=today).first()
            if not period:
                period = Period.objects.filter(end_date__lte=today).order_by('-end_date').first()

        return Ranking.objects.filter(current_rank__isnull=False, period=period).select_related('team')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today()

        context['confederations'] = Team.CONFEDERATION_CHOICES[:-1]
        context['periods'] = Period.objects.order_by('-start_date')
        context['period'] = Period.objects.filter(start_date__lte=today, end_date__gte=today).first()
        return context


class ConfederationRankingView(RankingView):

    def get_queryset(self):
        queryset = super().get_queryset()
        confederation = self.kwargs.get('conf', None)

        if confederation in dict(Team.CONFEDERATION_CHOICES):
            queryset = queryset.filter(team__confederation=confederation)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conf'] = self.kwargs.get('conf', None)
        return context


class StatisticsView(TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        today = datetime.today()
        context = super().get_context_data(**kwargs)

        rankings = Ranking.objects.annotate(
            rank_dif=F('previous_rank') - F('current_rank'),
            point_dif=F('current_points') - F('previous_points')
        )
        context.update({
            'top_movers': rankings.filter(rank_dif__gt=0).order_by('-rank_dif')[:10],
            'top_points_movers': rankings.filter(
                current_rank__isnull=False, point_dif__gt=0
            ).order_by('-point_dif')[:10],
            'top_fallers': rankings.filter(rank_dif__lt=0).order_by('rank_dif')[:10],
            'top_points_fallers': rankings.filter(
                current_rank__isnull=False, point_dif__lt=0
            ).order_by('point_dif')[:10],
            'periods': Period.objects.order_by('-start_date'),
            'period': Period.objects.filter(start_date__lte=today, end_date__gte=today).first()
        })
        return context
