from decimal import Decimal

from django.db import models

from apps.ranking.models import Period
from apps.team.models import Team


class League(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'leagues'
        verbose_name = 'League'
        verbose_name_plural = 'Leagues'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Competition(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    round = models.CharField(max_length=255)
    coefficient = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = 'competitions'
        verbose_name = 'Competition'
        verbose_name_plural = 'Competitions'
        ordering = ('-coefficient', 'league', 'round')

    def __str__(self):
        return f'{self.league}. {self.round}'


class Game(models.Model):
    ELO_DIVISOR = 600
    WIN = Decimal(1)
    DRAW = Decimal(0.5)
    LOSS = Decimal(0)

    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    is_knockout = models.BooleanField(default=False)

    home_team = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)

    home_goals = models.PositiveIntegerField()
    away_goals = models.PositiveIntegerField()

    home_points_change = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    away_points_change = models.DecimalField(max_digits=10, decimal_places=5, default=0)

    date = models.DateTimeField()
    is_calculated = models.BooleanField(default=False)

    class Meta:
        db_table = 'games'
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
        ordering = ('-date', )
        unique_together = ('home_team', 'away_team', 'date')
