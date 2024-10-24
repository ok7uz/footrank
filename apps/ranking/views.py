from datetime import datetime

from django.db.models import F
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, TemplateView

from apps.ranking.forms import TeamChangeForm, CompetitionChangeForm
from apps.ranking.models import Team, Competition, Game
from apps.ranking.permissions import StaffRequiredMixin


class RankingView(ListView):
    model = Team
    template_name = 'ranking.html'
    context_object_name = 'teams'
    paginate_by = 100

    def get_queryset(self):
        return Team.objects.filter(current_rank__isnull=False).prefetch_related('home_games', 'away_games')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confederations'] = Team.CONFEDERATION_CHOICES[:-1]
        context['current_date'] = datetime.today().strftime('%Y-%m-%d')
        return context


class ConfederationRankingView(RankingView):

    def get_queryset(self):
        confederation = self.kwargs.get('conf', None)
        if confederation and (confederation, confederation) in Team.CONFEDERATION_CHOICES:
            queryset = Team.objects.filter(
                current_rank__isnull=False,
                confederation=confederation).prefetch_related('home_games', 'away_games')
            return queryset
        return Team.objects.filter(current_rank__isnull=False).prefetch_related('home_games', 'away_games')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conf'] = self.kwargs.get('conf', None)
        return context


class CountryListView(ListView):
    model = Team
    template_name = 'country_list.html'
    context_object_name = 'teams'
    paginate_by = 100

    def get_queryset(self):
        confederation = self.request.GET.get('confederation')
        queryset = Team.objects.order_by('name')
        if confederation:
            queryset = queryset.filter(confederation=confederation)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confederations'] = Team.CONFEDERATION_CHOICES[:-1]
        return context


class CountryUpdateView(StaffRequiredMixin, TemplateView):
    model = Team
    pk_url_kwarg = 'country_code'
    template_name = 'country_update.html'
    form_class = TeamChangeForm

    def get(self, request, *args, **kwargs):
        team = self.get_object()
        form = self.form_class(instance=team)
        return self.render_to_response({'form': form, 'team': team})

    def post(self, request, *args, **kwargs):
        team = self.get_object()
        form = self.form_class(request.POST, instance=team)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('country_list')
        print(form.errors)
        return self.render_to_response({'form': form, 'team': team})

    def get_object(self):
        return Team.objects.get(country_code=self.kwargs.get(self.pk_url_kwarg))


class CompetitionListView(ListView):
    model = Team
    template_name = 'competition_list.html'
    context_object_name = 'competitions'

    def get_queryset(self):
        return Competition.objects.order_by('coefficient', 'league', 'round')


class CompetitionUpdateView(StaffRequiredMixin, TemplateView):
    model = Team
    pk_url_kwarg = 'competition_id'
    template_name = 'competition_update.html'
    form_class = CompetitionChangeForm

    def get(self, request, *args, **kwargs):
        team = self.get_object()
        form = self.form_class(instance=team)
        return self.render_to_response({'form': form, 'team': team})

    def post(self, request, *args, **kwargs):
        team = self.get_object()
        form = self.form_class(request.POST, instance=team)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('competition_list')
        print(form.errors)
        return self.render_to_response({'form': form, 'team': team})

    def get_object(self):
        print(self.kwargs.get(self.pk_url_kwarg))
        return Competition.objects.get(id=self.kwargs.get(self.pk_url_kwarg))


class NotCompletedGameView(ListView):
    template_name = 'not_completed.html'
    context_object_name = 'games'

    def get_queryset(self):
        return {
            'past_games': Game.objects.filter(date__lt=datetime.now()).order_by(
                'date__year',
                'date__month',
                'date__day',
                'competition'
            ),
            'fixtures': Game.objects.filter(date__gt=datetime.now()).order_by(
                'date__year',
                'date__month',
                'date__day',
                'competition'
            )
        }


def calculate_games(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game.calculate()
    return redirect('game_list')


def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game.delete()
    return redirect('game_list')


class StatisticsView(TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams = Team.objects.annotate(
            rank_dif=F('previous_rank') - F('current_rank'),
            point_dif=F('current_points') - F('previous_points')
        )
        context['top_movers'] = teams.filter(rank_dif__gt=0).order_by('-rank_dif')[:10]
        context['top_points_movers'] = teams.filter(
            current_rank__isnull=False, point_dif__gt=0
        ).order_by('-point_dif')[:10]
        context['top_fallers'] = teams.filter(rank_dif__lt=0).order_by('rank_dif')[:10]
        context['top_points_fallers'] = teams.filter(
            current_rank__isnull=False, point_dif__lt=0
        ).order_by('point_dif')[:10]
        return context
