import uuid

from django.db import models

from apps.team.models import Team


class Period(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'periods'
        verbose_name = 'Period'
        verbose_name_plural = 'Periods'
        ordering = ('start_date', )

    def __str__(self):
        return f'{self.start_date.strftime('%d %B, %Y')} - {self.end_date.strftime('%d %B, %Y')}'


class Ranking(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='rankings')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='rankings')
    current_rank = models.PositiveIntegerField(null=True, db_index=True)
    previous_rank = models.PositiveIntegerField(null=True, db_index=True)
    current_points = models.DecimalField(max_digits=10, decimal_places=5)
    previous_points = models.DecimalField(max_digits=10, decimal_places=5)

    class Meta:
        unique_together = ('team', 'period')
        ordering = ['current_rank']

    @property
    def rank_difference(self):
        if self.current_rank and self.previous_rank:
            return self.previous_rank - self.current_rank
        return None

    @property
    def point_difference(self):
        if self.current_points and self.previous_points:
            return self.current_points - self.previous_points
        return None

    def games(self, period: Period):
        return self.home_games.filter(period=period).all() | self.away_games.filter(period=period).all()

    def __str__(self):
        return f'Ranking for {self.team} in {self.period}'
