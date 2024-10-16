from django.contrib import admin

from .models import Team, Game, Period, Competition


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_rank', 'current_points')


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'coefficient')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('home_team',  'home_goals', 'away_goals', 'away_team', 'date')
    fields = ('competition', 'home_team', 'away_team', 'home_goals', 'away_goals', 'date', 'home_points_change', 'away_points_change')
    readonly_fields = ('home_points_change', 'away_points_change')


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date')
