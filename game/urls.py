from django.urls import path
from .views import GameListView, GameDetailView, FetchIGDBGames

urlpatterns = [
    path('', GameListView.as_view()), 
    path('<int:pk>/', GameDetailView.as_view()),
    path('fetch-igdb-games/', FetchIGDBGames.as_view(), name='fetch_igdb_games'),
]