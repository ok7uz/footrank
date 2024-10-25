from django.db import models


class Team(models.Model):
    CONFEDERATION_CHOICES = [
        ('UEFA', 'UEFA'),
        ('AFC', 'AFC'),
        ('OFC', 'OFC'),
        ('CONMEBOL', 'CONMEBOL'),
        ('CAF', 'CAF'),
        ('CONCACAF', 'CONCACAF'),
    ]

    name = models.CharField(max_length=255, unique=True)
    country_code = models.CharField(primary_key=True, max_length=3)
    flag_url = models.URLField(verbose_name='Flag URL', null=True)
    confederation = models.CharField(max_length=10, choices=CONFEDERATION_CHOICES, db_index=True)
    api_id = models.PositiveIntegerField(unique=True, null=True, db_index=True, verbose_name='API ID')

    class Meta:
        db_table = 'teams'
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ('name', )

    def games(self, period):
        return self.home_games.filter(period=period).all() | self.away_games.filter(period=period).all()

    def __str__(self):
        return self.name
