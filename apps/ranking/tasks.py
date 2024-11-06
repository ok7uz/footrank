import datetime
import time

import requests
from decimal import Decimal
from celery import shared_task
from decouple import config
from django.db import transaction

from .models import Team, Period, Ranking
from ..game.models import League, Competition, Game

FIXTURES_URL = "https://v3.football.api-sports.io/fixtures?date={}"


@shared_task
def fetch_matches(date=None, is_finished=True, api_key=config('FOOTBALL_API_KEY1')):
    today_date = date or datetime.date.today().strftime("%Y-%m-%d")
    yesterday_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    headers = {'x-apisports-key': api_key}

    today_response = requests.get(FIXTURES_URL.format(today_date), headers=headers)
    time.sleep(5)
    yesterday_response = requests.get(FIXTURES_URL.format(yesterday_date), headers=headers)

    data = today_response.json().get('response', []) + yesterday_response.json().get('response', [])
    for fixture in data:
        status = fixture['fixture']['status']['short']
        tournament = fixture['league']['name']
        tournament_round = fixture['league']['round'].split('-')[0].strip()
        home_team_data = fixture['teams']['home']
        away_team_data = fixture['teams']['away']
        home_goals = fixture['goals']['home']
        away_goals = fixture['goals']['away']
        date = fixture['fixture']['date']

        home_team = Team.objects.filter(api_id=home_team_data['id']).first()
        away_team = Team.objects.filter(api_id=away_team_data['id']).first()
        period = Period.objects.filter(start_date__lte=date, end_date__gte=date).first()

        if (not is_finished or status == 'FT') and home_team and away_team:
            league, _ = League.objects.get_or_create(name=tournament)
            competition, _ = Competition.objects.get_or_create(league=league, round=tournament_round)
            Game.objects.get_or_create(
                period=period,
                competition=competition,
                home_team=home_team,
                away_team=away_team,
                home_goals=home_goals,
                away_goals=away_goals,
                date=date
            )


@shared_task
def fetch_fixtures(date=None):
    start_date = date or datetime.date.today()

    for i in range(1, 10):
        request_date = (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        fetch_matches(request_date, is_finished=False, api_key=config('FOOTBALL_API_KEY2'))
        time.sleep(5)


@shared_task
def calculate_matches_points():
    games = Game.objects.filter(is_calculated=False, date__lt=datetime.datetime.now()).order_by('date')
    for game in games:
        home_ranking = Ranking.objects.get(period=game.period, team=game.home_team)
        away_ranking = Ranking.objects.get(period=game.period, team=game.away_team)

        if game.competition.coefficient:
            home_points_change, away_points_change = calculate_points_change(game)
            with transaction.atomic():
                game.home_points_change = home_points_change
                game.away_points_change = away_points_change
                game.is_calculated = True
                game.save()

                home_ranking.current_points += home_points_change
                away_ranking.current_points += away_points_change
                home_ranking.save()
                away_ranking.save()


@shared_task
def ranking_everyday():
    today = datetime.date.today()
    period = Period.objects.filter(start_date__lte=today, end_date__gte=today).first()
    rankings = Ranking.objects.filter(current_rank__isnull=False, period=period).order_by('-current_points')

    for index, ranking in enumerate(rankings, start=1):
        ranking.current_rank = index
        ranking.save()


def calculate_points_change(game: Game):
    home_ranking = Ranking.objects.get(period=game.period, team=game.home_team)
    away_ranking = Ranking.objects.get(period=game.period, team=game.away_team)

    delta = home_ranking.current_points - away_ranking.current_points
    win_home = game.WIN if game.home_goals > game.away_goals else game.LOSS if game.home_goals < game.away_goals else game.DRAW
    win_away = 1 - win_home
    expected_win_home = 1 / (10 ** (- delta / game.ELO_DIVISOR) + 1)
    expected_win_away = 1 / (10 ** (delta / game.ELO_DIVISOR) + 1)
    return (
        game.competition.coefficient * (Decimal(win_home) - expected_win_home),
        game.competition.coefficient * (Decimal(win_away) - expected_win_away)
    )


@shared_task
def create_ranking_for_new_period():
    current_date = datetime.date.today()
    current_period = Period.objects.filter(start_date=current_date).first()
    previous_period = Period.objects.filter(end_date=current_date - datetime.timedelta(days=1)).first()

    if current_period and previous_period:
        current_rankings = Ranking.objects.all()

        for ranking in current_rankings:
            Ranking.objects.create(
                team=ranking.team,
                period=current_period,
                current_rank=ranking.current_rank,
                previous_rank=ranking.current_rank,
                current_points=ranking.current_points,
                previous_points=ranking.current_points,
            )
