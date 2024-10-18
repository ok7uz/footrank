import datetime
import requests
from celery import shared_task
from decouple import config

from .models import Competition, League, Game, Team


FIXTURES_URL = "https://v3.football.api-sports.io/fixtures"


@shared_task
def fetch_matches(date=None):
    today_date = date or datetime.date.today().strftime("%Y-%m-%d")
    yesterday_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    headers = {'x-apisports-key': config('FOOTBALL_API_KEY')}
    today_response = requests.get(FIXTURES_URL.format(today_date), headers=headers)
    yesterday_response = requests.get(FIXTURES_URL.format(yesterday_date), headers=headers)
    data = today_response.json()['response'] + yesterday_response.json()['response']

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

        if status == 'FT' and home_team and away_team:
            league, _ = League.objects.get_or_create(name=tournament)
            competition, _ = Competition.objects.get_or_create(league=league, round=tournament_round)
            Game.objects.create(
                competition=competition,
                home_team=home_team,
                away_team=away_team,
                home_goals=home_goals,
                away_goals=away_goals,
                date=date
            )


@shared_task
def calculate_matches_points():
    games = Game.objects.filter(is_calculated=False).order_by('date')
    for game in games:
        tournament = game.competition

        if tournament.coefficient:
            game.home_points_change = calculate_points_change(game)
            game.away_points_change = calculate_points_change(game)
            game.save()

            game.home_team.current_points += game.home_points_change
            game.away_team.current_points += game.away_points_change
            game.home_team.save()
            game.away_team.save()


@shared_task
def ranking():
    teams = Team.objects.filter(current_rank__isnull=False).order_by('-current_points')

    for index, team in enumerate(teams, start=1):
        team.current_rank = index
        team.save()


def calculate_points_change(game: Game):
    delta = game.home_team.current_points - game.away_team.current_points
    win = 1 if game.home_goals > game.away_goals else 0 if game.home_goals < game.away_goals else 0.5
    expected_win = 1 / (10 ** (- delta / 600) + 1)
    return game.competition.coefficient * (win - expected_win)
