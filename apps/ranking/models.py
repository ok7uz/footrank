from decimal import Decimal

from django.db import models


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
    flag_url = models.URLField(verbose_name='Flag URL')
    current_rank = models.PositiveIntegerField(null=True, db_index=True)
    previous_rank = models.PositiveIntegerField(null=True, db_index=True)
    current_points = models.DecimalField(max_digits=10, decimal_places=5)
    previous_points = models.DecimalField(max_digits=10, decimal_places=5)
    confederation = models.CharField(max_length=10, choices=CONFEDERATION_CHOICES, default='N/A', db_index=True)
    api_id = models.PositiveIntegerField(unique=True, null=True, db_index=True, verbose_name='API ID')

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
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    is_knockout = models.BooleanField(default=False)

    home_team = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)

    home_goals = models.PositiveIntegerField()
    away_goals = models.PositiveIntegerField()

    home_points_change = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    away_points_change = models.DecimalField(max_digits=10, decimal_places=5, default=0)

    date = models.DateField()
    is_calculated = models.BooleanField(default=False)

    def calculate(self) -> None:
        delta = self.home_team.current_points - self.away_team.current_points
        expected_home_win = 1 / (10 ** (-delta / 600) + 1)
        expected_away_win = 1 / (10 ** (delta / 600) + 1)
        win = 1 if self.home_goals > self.away_goals else 0 if self.home_goals < self.away_goals else 0.5
        self.home_points_change = (Decimal(win) - expected_home_win) * self.competition.coefficient
        self.away_points_change = (Decimal(1 - win) - expected_away_win) * self.competition.coefficient
        self.home_team.current_points += self.home_points_change
        self.away_team.current_points += self.away_points_change
        self.home_team.save()
        self.away_team.save()
        self.is_calculated = True
        self.save()

        teams = Team.objects.filter(current_rank__isnull=False)
        for index, team in enumerate(teams, start=1):
            team.current_rank = index
            team.save()

    class Meta:
        db_table = 'games'
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
        ordering = ('-date', )
        unique_together = ('home_team', 'away_team', 'date')


class Period(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'periods'
        verbose_name = 'Period'
        verbose_name_plural = 'Periods'
        ordering = ('start_date', )
