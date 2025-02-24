from django.urls import path
from .views import GameListView, GameDetailView

urlpatterns = [
    path('', GameListView.as_view()), 
    path('<int:pk>/', GameDetailView.as_view())
]