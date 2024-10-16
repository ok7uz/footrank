from django.contrib import admin

from .models import Competition, Game, Team, League


admin.site.register(Competition)
admin.site.register(Game)
admin.site.register(Team)
admin.site.register(League)
