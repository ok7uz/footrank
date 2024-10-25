from datetime import datetime
from lib2to3.fixes.fix_input import context

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from apps.ranking.models import Period, Ranking
from apps.team.models import Team


class TeamDetailView(DetailView):
    model = Team
    pk_url_kwarg = 'country_code'
    context_object_name = 'team'
    template_name = 'team-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        period_id = self.request.GET.get('period', None)
        today = datetime.today()

        period = get_object_or_404(Period, id=period_id) if period_id else None
        if not period:
            period = Period.objects.filter(start_date__lte=today, end_date__gte=today).first()
            if not period:
                period = Period.objects.filter(end_date__lte=today).order_by('-end_date').first()

        context['ranking'] = Ranking.objects.get(team=context['team'], period=period)
        context['periods'] = Period.objects.order_by('-start_date')
        context['period'] = Period.objects.filter(start_date__lte=today, end_date__gte=today).first()
        context['games'] = context['team'].games(period)
        return context

