from django.urls import path

from apps.ranking import views


urlpatterns = [
    path('countries', views.CountryListView.as_view(), name='country_list'),
    path('countries/<str:country_code>', views.CountryUpdateView.as_view(), name='country_update'),

    path('competitions', views.CompetitionListView.as_view(), name='competition_list'),
    path('competitions/<int:competition_id>', views.CompetitionUpdateView.as_view(), name='competition_update'),

    path('games', views.NotCompletedGameView.as_view(), name='game_list'),
    path('games/<int:game_id>/calculate', views.calculate_games, name='calculate_games'),
    path('games/<int:game_id>/delete', views.delete_game, name='delete_game'),

    path('ranking', views.RankingView.as_view(), name='ranking'),
    path('ranking/<str:conf>', views.ConfederationRankingView.as_view(), name='conf-ranking'),

    path('statistics', views.StatisticsView.as_view(), name='statistics'),
]
