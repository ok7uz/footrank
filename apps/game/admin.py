from django.contrib import admin

from apps.game import models


@admin.register(models.League)
class LeagueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Competition)
class CompetitionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    pass
