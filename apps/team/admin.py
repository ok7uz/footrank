from django.contrib import admin

from apps.team import models


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ('name', )
