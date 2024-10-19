from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, TemplateView

from apps.ranking.forms import TeamChangeForm, CompetitionChangeForm
from apps.ranking.models import Team, Competition, Game


class RankingView(ListView):
    model = Team
    template_name = 'ranking.html'
    context_object_name = 'teams'

    def get_queryset(self):
        confederation = self.request.GET.get('confederation')
        queryset = Team.objects.filter(current_rank__isnull=False)
        if confederation:
            queryset = queryset.filter(confederation=confederation)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confederations'] = Team.CONFEDERATION_CHOICES[:-1]
        return context


class CountryListView(ListView, PermissionRequiredMixin):
    model = Team
    template_name = 'country_list.html'
    context_object_name = 'teams'

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


class CountryUpdateView(TemplateView, PermissionRequiredMixin):
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


class CompetitionListView(ListView, PermissionRequiredMixin):
    model = Team
    template_name = 'competition_list.html'
    context_object_name = 'competitions'

    def get_queryset(self):
        return Competition.objects.order_by('coefficient', 'league', 'round')


class CompetitionUpdateView(TemplateView, PermissionRequiredMixin):
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
        return Game.objects.all().order_by(
            'date__year',
            'date__month',
            'date__day',
            'competition'
        )


def calculate_games(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game.calculate()
    return redirect('game_list')


def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game.delete()
    return redirect('game_list')
