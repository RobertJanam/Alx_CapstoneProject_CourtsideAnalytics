from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.TeamListView.as_view(), name='team-list'),
    path('teams/join/', views.JoinTeamView.as_view(), name='team-join'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('teams/<int:team_id>/members/', views.TeamMembersView.as_view(), name='team-members'),
    path('teams/<int:team_id>/members/<int:member_id>/update/', views.TeamMemberUpdateView.as_view(), name='team-member-update')
]