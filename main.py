import requests


url = 'https://inside.fifa.com/api/ranking-overview?locale=en&dateId=id14506'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.fifa.com/rankings',
}


def run():
    from apps.ranking.models import Team
    response = requests.get(url, headers=headers)
    print(response.text)
    data = response.json()
    for team in data['rankings']:
        Team.objects.update_or_create(
            name=team['rankingItem']['name'],
            country_code=team['rankingItem']['countryCode'],
            flag_url=team['rankingItem']['flag']['src'],
            current_rank=team['rankingItem']['rank'],
            previous_rank=team['rankingItem']['rank'],
            current_points=team['rankingItem']['totalPoints'],
            previous_points=team['totalPoints'],
            confederation=team['tag']['text'],
        )
    print('Done')

