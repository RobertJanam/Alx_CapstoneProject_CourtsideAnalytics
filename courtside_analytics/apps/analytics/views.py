# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from apps.teams.models import Team, TeamMember
from apps.games.models import PlayerStat, Game
from .utils import get_player_averages, get_team_leaderboard, get_team_trends

class PlayerAnalyticsView(APIView):
    #Get analytics for a specific player
    #GET/api/analytics/players/{player_id}/

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, player_id):
        team_id = request.query_params.get('team_id')

        # verify that the user has access to this player's team
        if team_id:
            team = get_object_or_404(Team, id=team_id)
            if not TeamMember.objects.filter(user=request.user, team=team, is_active=True).exists():
                raise PermissionDenied("You don't have access to this team's data")

        averages = get_player_averages(player_id, team_id)
        return Response(averages)

class TeamLeaderboardView(APIView):
    #Get team leaderboard by stat.
    #GET/api/analytics/teams/{team_id}/leaderboard/

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, team_id):
        # see if user is a member
        team = get_object_or_404(Team, id=team_id)
        if not TeamMember.objects.filter(user=request.user, team=team, is_active=True).exists():
            raise PermissionDenied("You are not a member of this team")

        ppg = request.query_params.get('ppg', 'points')
        ast = request.query_params.get('ast', 'assists')
        rbd = request.query_params.get('rbd', 'rebounds')
        stl = request.query_params.get('stl', 'steals')
        blc = request.query_params.get('blc', 'blocks')
        limit = int(request.query_params.get('limit', 10))

        # validate stat
        allowed_stats = ['points', 'assists', 'rebounds', 'steals', 'blocks']
        if ppg not in allowed_stats or ast not in allowed_stats or rbd not in allowed_stats or stl not in allowed_stats or blc not in allowed_stats:
            return Response(
                {"error": f"Stat must be one of: {', '.join(allowed_stats)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        leaderboard = get_team_leaderboard(team_id, ppg, ast, rbd, stl, blc, limit)
        return Response({
            'team': team.name,
            'ppg': ppg,
            'ast': ast,
            'rbd': rbd,
            'stl': stl,
            'blc': blc,
            'leaderboard': leaderboard
        })

class TeamTrendsView(APIView):
    # Get team performance trends.
    # GET/api/analytics/teams/{team_id}/trends/

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, team_id):
        # Check if user is a member
        team = get_object_or_404(Team, id=team_id)
        if not TeamMember.objects.filter(user=request.user, team=team, is_active=True).exists():
            raise PermissionDenied("You are not a member of this team")

        trends = get_team_trends(team_id)
        trends['team'] = team.name
        return Response(trends)

class GameAnalyticsView(APIView):
    # Get analytics for a specific game.
    # GET/api/analytics/games/{game_id}/

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)

        # Verify user is a member
        if not TeamMember.objects.filter(user=request.user, team=game.team, is_active=True
        ).exists():
            raise PermissionDenied("You are not a member of this team")

        # Get all player stats for this game
        stats = PlayerStat.objects.filter(game=game).select_related('player__user')

        # Calculate team totals
        team_total = {
            'points': sum(s.points for s in stats),
            'assists': sum(s.assists for s in stats),
            'rebounds': sum(s.rebounds for s in stats),
            'steals': sum(s.steals for s in stats),
            'blocks': sum(s.blocks for s in stats),
            'turnovers': sum(s.turnovers for s in stats),
            'fouls': sum(s.fouls for s in stats),
        }

        # Find top performers
        top_scorer = max(stats, key=lambda s: s.points) if stats else None

        return Response({
            'game': {
                'id': game.id,
                'date': game.game_date,
                'opponent': game.opponent_name,
                'score': f"{game.team_score}-{game.opponent_score}",
                'winner': game.winner,
                'margin': game.margin
            },
            'team_totals': team_total,
            'top_scorer': {
                'player': top_scorer.player.user.username if top_scorer else None,
                'points': top_scorer.points if top_scorer else 0
            } if top_scorer else None,
            'player_stats': [{
                'player': s.player.user.username,
                'position': s.player.position,
                'points': s.points,
                'assists': s.assists,
                'rebounds': s.rebounds,
                'steals': s.steals,
                'blocks': s.blocks,
                'efficiency': s.efficiency
            } for s in stats]
        })
