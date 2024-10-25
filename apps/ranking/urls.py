from django.urls import path

from apps.ranking import views


urlpatterns = [
    path('ranking', views.RankingView.as_view(), name='ranking'),
    path('ranking/<str:conf>', views.ConfederationRankingView.as_view(), name='conf-ranking'),

    path('statistics', views.StatisticsView.as_view(), name='statistics'),
]
