from django.urls import path
from .views import UserGameListView, UserGameDetailView, SaveGameView, UserGameByStatusView

urlpatterns = [
    path('', UserGameListView.as_view(), name='usergame-list'),
    path('<int:pk>/', UserGameDetailView.as_view(), name='usergame-detail'),
    path('save-game/', SaveGameView.as_view(), name='save_game'), 
    path('usergames/status/<str:status_type>/', UserGameByStatusView.as_view(), name='usergames-by-status'),
]
