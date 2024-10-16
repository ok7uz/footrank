from decimal import Decimal
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Team(models.Model):
    CONFEDERATION_CHOICES = [
        ('UEFA', 'UEFA'),
        ('AFC', 'AFC'),
        ('OFC', 'OFC'),
        ('CONMEBOL', 'CONMEBOL'),
        ('CAF', 'CAF'),
        ('CONCACAF', 'CONCACAF'),
        ('N/A', 'Not Applicable'),
    ]

    name = models.CharField(max_length=255, unique=True)
    country_code = models.CharField(primary_key=True, max_length=3, unique=True)
    flag_url = models.URLField()
    current_rank = models.PositiveIntegerField(null=True, db_index=True)
    previous_rank = models.PositiveIntegerField(null=True, db_index=True)
    current_points = models.DecimalField(max_digits=10, decimal_places=5)
    previous_points = models.DecimalField(max_digits=10, decimal_places=5)
    confederation = models.CharField(max_length=10, choices=CONFEDERATION_CHOICES, default='N/A', db_index=True)

    @property
    def rank_difference(self):
        return self.previous_rank - self.current_rank

    @property
    def points_difference(self):
        return self.current_points - self.previous_points

    @property
    def games(self):
        return self.home_games.all() | self.away_games.all()

    class Meta:
        db_table = 'teams'
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ('current_rank', )

    def __str__(self):
        return self.name


class Competition(models.Model):
    name = models.CharField(max_length=255, unique=True)
    coefficient = models.PositiveIntegerField()

    class Meta:
        db_table = 'competitions'
        verbose_name = 'Competition'
        verbose_name_plural = 'Competitions'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Game(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    is_knockout = models.BooleanField(default=False)

    home_team = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)

    home_goals = models.PositiveIntegerField()
    away_goals = models.PositiveIntegerField()

    home_points_change = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    away_points_change = models.DecimalField(max_digits=10, decimal_places=5, default=0)

    date = models.DateField()

    class Meta:
        db_table = 'games'
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
        ordering = ('-date', )

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        delta = self.home_team.current_points - self.away_team.current_points
        home_we = 1 / (10 ** (-delta / 600) + 1)
        away_we = 1 / (10 ** (delta / 600) + 1)
        w = 1 if self.home_goals > self.away_goals else 0.5 if self.home_goals == self.away_goals else 0
        home_points_change = self.competition.coefficient * (Decimal(w) - home_we)
        away_points_change = self.competition.coefficient * (Decimal(1 - w) - away_we)
        self.home_points_change = home_points_change
        self.away_points_change = away_points_change

        if not self.id:
            self.home_team.current_points += home_points_change
            self.away_team.current_points += away_points_change
            self.home_team.save()
            self.away_team.save()

        return super().save(*args, force_insert, force_update, using, update_fields)


@receiver(post_save, sender=Game)
def update_team_ranking(sender, instance, created, **kwargs):
    teams = Team.objects.filter(current_rank__isnull=False).order_by('-current_points')
    for index, team in enumerate(teams):
        team.current_rank = index + 1
        team.save()


class Period(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'periods'
        verbose_name = 'Period'
        verbose_name_plural = 'Periods'
        ordering = ('start_date', )
