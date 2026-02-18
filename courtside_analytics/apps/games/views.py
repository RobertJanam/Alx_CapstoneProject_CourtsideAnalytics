from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Game, PlayerStat
from apps.teams.models import Team, TeamMember
from .serializers import (
    GameSerializer,
    GameDetailSerializer,
    PlayerStatSerializer
)


# Create your views here.
class GameListView(generics.ListCreateAPIView):
    # API endpoint for listing team games and creating new games
    # GET/api/teams/{team_id}/games/: List all games for a team
    # POST/api/teams/{team_id}/games/: create a new game (only coaches)

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        team = get_object_or_404(Team, id=team_id)

        if not TeamMember.objects.filter(
            user=self.request.user, team=team,
            is_active=True).exists():
            raise PermissionDenied("You are not a member of this team.")

        return Game.objects.filter(team=team)

    def perform_create(self, serializer):
        team_id = self.kwargs['team_id']
        team = get_object_or_404(Team, id=team_id)

        if not TeamMember.objects.filter(
            user=self.request.user, team=team,
            role='COACH', is_active=True
        ).exists():
            raise PermissionDenied("Only coaches can add games.")

        #save game
        serializer.save(
            team=team,
            recorded_by=self.request.user
        )


class GameDetailView(generics.RetrieveUpdateDestroyAPIView):
    # API endpoint for viewing, updating or deleting a specific game.
    # GET/api/games/{id}/: for viewing game details
    # PUT/api/games/{id}/: for updating game (for coach only use)
    # DELETE/api/games/{id}/: for deleting game (for coach only use)

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GameDetailSerializer
        return GameSerializer

    def get_queryset(self):
        return Game.objects.all()

    def get_object(self):
        game = super().get_object()

        if not TeamMember.objects.filter(
            user=self.request.user, team=game.team,
            is_active=True).exists():
            raise PermissionDenied("You are not a member of this team.")

        return game

    def perform_update(self, serializer):
        game = self.get_object()

        if not TeamMember.objects.filter(
            user=self.request.user, team=game.team,
            role='COACH', is_active=True
        ).exists():
            raise PermissionDenied("Only coaches can update games.")

        serializer.save()

    def perform_destroy(self, instance):
        if not TeamMember.objects.filter(
            user=self.request.user, team=instance.team,
            role='COACH', is_active=True
        ).exists():
            raise PermissionDenied("Only coaches can delete games.")

        instance.delete()


class PlayerStatView(generics.CreateAPIView):
    # API endpoint for adding player statistics to a game
    # POST/api/games/{game_id}/stats/
    # request body contains player stats for one player

    serializer_class = PlayerStatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        game_id = self.kwargs['game_id']
        game = get_object_or_404(Game, id=game_id)

        # verify that the user is a coach of this team
        if not TeamMember.objects.filter(
            user=self.request.user,
            team=game.team,
            role='COACH',
            is_active=True
        ).exists():
            raise PermissionDenied("Only coaches can add player stats.")

        # verify that the player belongs to this team
        player_id = self.request.data.get('player')
        if player_id:
            if not TeamMember.objects.filter(
                id=player_id,
                team=game.team,
                is_active=True
            ).exists():
                raise PermissionDenied("This player is not a member of the team.")

        serializer.save(game=game)


class PlayerStatsListView(generics.ListAPIView):
    # API endpoint for listing all player stats for a game
    # GET/api/games/{game_id}/stats/
    # All team members can view stats

    serializer_class = PlayerStatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        game_id = self.kwargs['game_id']
        game = get_object_or_404(Game, id=game_id)

        # verify user is a member of this team
        if not TeamMember.objects.filter(
            user=self.request.user,
            team=game.team,
            is_active=True
        ).exists():
            raise PermissionDenied("You are not a member of this team.")

        return PlayerStat.objects.filter(game=game).select_related('player__user')