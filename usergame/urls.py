from django.urls import path
from .views import UserGameListView, UserGameDetailView, SaveGameView, UserGameByStatusView, FullGameDetailView

urlpatterns = [
    path('', UserGameListView.as_view(), name='usergame-list'),
    path('<int:pk>/', UserGameDetailView.as_view(), name='usergame-detail'),
    path('save-game/', SaveGameView.as_view(), name='save_game'), 
    path('status/<str:page_status_type>/', UserGameByStatusView.as_view(), name='usergames-by-status'),
    path('<int:pk>/full/', FullGameDetailView.as_view(), name='fullusergame'),

]
