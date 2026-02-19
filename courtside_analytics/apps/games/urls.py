from django.urls import path
from . import views

urlpatterns = [
    path('teams/<int:team_id>/games/', views.GameListView.as_view(), name='game-list'),
    path('games/<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),
    path('games/<int:game_id>/stats', views.PlayerStatsListView.as_view(), name='stats-list'),
    path('games/<int:game_id>/stats/add', views.PlayerStatView.as_view(), name='stats-add'),
]