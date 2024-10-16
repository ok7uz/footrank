from django.urls import path

from apps.ranking import views


urlpatterns = [
    path('', views.RankingView.as_view(), name='ranking'),
    # path('countries/<str:country_code>/', views.CountryView.as_view(), name='country'),
]
