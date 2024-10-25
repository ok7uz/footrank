from django.contrib import admin

from apps.ranking import models


@admin.register(models.Ranking)
class RankingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Period)
class PeriodAdmin(admin.ModelAdmin):
    pass
