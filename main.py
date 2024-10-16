import requests
from decouple import config
from django.db import transaction

from apps.ranking.models import Game, Team, Competition, League


def run(date='2024-10-15'):
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': config('FOOTBALL_API_KEY')
    }

    response = requests.get(f"https://v3.football.api-sports.io/fixtures?date={date}", headers=headers)
    data = response.json()['response']

    for game in data:
        with transaction.atomic():
            date = game['fixture']['date'][:10]
            status = game['fixture']['status']['short']
            league = game['league']['name']
            league_round = game['league']['round']
            home_team_name = game['teams']['home']['name']
            away_team_name = game['teams']['away']['name']
            home_goals = game['goals']['home']
            away_goals = game['goals']['away']
            home_team_id = game['teams']['home']['id']
            away_team_id = game['teams']['away']['id']

            if Team.objects.filter(api_id=home_team_id).exists() and Team.objects.filter(api_id=away_team_id).exists() and status == 'FT':

                home_team = Team.objects.get(api_id=home_team_id)
                away_team = Team.objects.get(api_id=away_team_id)

                league, _ = League.objects.get_or_create(name=league)
                competition, _ = Competition.objects.get_or_create(league=league, round=league_round)
                game, created = Game.objects.get_or_create(
                    date=date,
                    competition=competition,
                    home_team=home_team,
                    away_team=away_team,
                    home_goals=home_goals,
                    away_goals=away_goals
                )

