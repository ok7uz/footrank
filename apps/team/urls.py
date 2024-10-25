from django.urls import path

from apps.team import views

urlpatterns = [
    path('teams/<str:country_code>', views.TeamDetailView.as_view(), name='team-detail'),
]
