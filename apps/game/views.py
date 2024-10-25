from datetime import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from apps.game.models import Game
from apps.ranking.models import Period


class GameListView(ListView):
    model = Game
    context_object_name = 'games'
    template_name = 'games.html'

    def get_queryset(self):
        period_id = self.request.GET.get('period', None)
        today = datetime.today()

        period = get_object_or_404(Period, id=period_id) if period_id else None
        if not period:
            period = Period.objects.filter(start_date__lte=today, end_date__gte=today).first()
            if not period:
                period = Period.objects.filter(end_date__lte=today).order_by('-end_date').first()

        return Game.objects.filter(period=period).select_related('competition', 'home_team', 'away_team')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today()
        context['periods'] = Period.objects.order_by('-start_date')
        context['period'] = Period.objects.filter(start_date__lte=today, end_date__gte=today).first()
        return context
