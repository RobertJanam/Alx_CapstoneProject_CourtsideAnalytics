from django.urls import path
from . import views

urlpatterns = [
    # for player analytics
    path('analytics/players/<int:player_id>/', views.PlayerAnalyticsView.as_view(), name='player-analytics'),
    # for team analytics
    path('analytics/teams/<int:team_id>/leaderboard/', views.TeamLeaderboardView.as_view(), name='team-leaderboard'),
    path('analytics/teams/<int:team_id>/trends/', views.TeamTrendsView.as_view(), name='team-trends'),
    # for game analytics
    path('analytics/games/<int:game_id>/', views.GameAnalyticsView.as_view(), name='game-analytics'),
]

