from django.urls import path
from .views import UserGameListView, UserGameDetailView

urlpatterns = [
    path('', UserGameListView.as_view(), name='usergame-list'),
    path('<int:pk>/', UserGameDetailView.as_view(), name='usergame-detail'),
]
