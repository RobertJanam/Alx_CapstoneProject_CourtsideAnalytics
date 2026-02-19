from django.urls import path
from . import views

url_patterns = [
    path('teams/', views.TeamListView.as_view(), name='team-list'),
    path('teams/join/', views.JoinTeamView.as_view, name='team-join'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('teams/<int:team_id>/members/', views.TeamMembersView.as_view(), name='team-members'),
]