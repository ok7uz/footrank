from django.urls import path

from apps.game import views

urlpatterns = [
    path('games', views.GameListView.as_view(), name='games'),
]