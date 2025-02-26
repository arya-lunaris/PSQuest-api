from django.urls import path
from .views import UserGameListView, UserGameDetailView, SaveGameView

urlpatterns = [
    path('', UserGameListView.as_view(), name='usergame-list'),
    path('<int:pk>/', UserGameDetailView.as_view(), name='usergame-detail'),
    path('save-game/', SaveGameView.as_view(), name='save_game'), 
]
