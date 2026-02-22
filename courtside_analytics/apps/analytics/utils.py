from django.db.models import Avg, Sum, Count, Q, F
from apps.games.models import PlayerStat, Game
from apps.teams.models import Team, TeamMember

def get_player_averages(player_id, team_id=None):
    # calculate the avg stat for a player
    queryset = PlayerStat.objects.filter(player_id=player_id)

    if team_id:
        queryset = queryset.filter(game__team_id=team_id)

    totals = queryset.aggregate(
        games_played=Count('id'),
        avg_points=Avg('points'),
        avg_assists=Avg('assists'),
        avg_rebounds=Avg('rebounds'),
        avg_steals=Avg('steals'),
        avg_blocks=Avg('blocks'),
        total_points=Sum('points'),
        total_assists=Sum('assists'),
        total_rebounds=Sum('rebounds'),
        total_steals=Sum('steals'),
        total_blocks=Sum('blocks'),
    )

    # calculate per-game avg
    games = totals['games_played'] or 1  # avoid div by zero
    return {
        'games_played': totals['games_played'] or 0,
        'ppg': round(totals['avg_points'] or 0, 1),
        'apg': round(totals['avg_assists'] or 0, 1),
        'rpg': round(totals['avg_rebounds'] or 0, 1),
        'spg': round(totals['avg_steals'] or 0, 1),
        'bpg': round(totals['avg_blocks'] or 0, 1),
        'total_points': totals['total_points'] or 0,
    }

def get_team_leaderboard(team_id, stat='points', limit=10):
    # get the team leaderboard for a specific stat
    players = TeamMember.objects.filter(
        team_id=team_id, is_active=True, role='PLAYER').annotate(
        total_stat=Sum(f'game_stats__{stat}'),
        games_played=Count('game_stats', distinct=True),
        avg_stat=Avg(f'game_stats__{stat}')).filter(games_played__gt=0).order_by('-total_stat')[:limit]

    return [{
        'player_id': p.id,
        'player_name': p.user.username,
        'position': p.position,
        'jersey_number': p.jersey_number,
        f'total_{stat}': p.total_stat or 0,
        f'avg_{stat}': round(p.avg_stat or 0, 1),
        'games_played': p.games_played
    } for p in players]

def get_team_trends(team_id):
    # used for getting team performance trend over time
    games = Game.objects.filter(team_id=team_id).order_by('game_date')

    if not games.exists():
        return {}

    # calculate averages
    avg_points = games.aggregate(avg=Avg('team_score'))['avg'] or 0
    avg_allowed = games.aggregate(avg=Avg('opponent_score'))['avg'] or 0

    # best and worst games
    best_game = games.order_by('-team_score').first()
    worst_game = games.order_by('team_score').first()

    # Win/Loss record
    wins = games.filter(team_score__gt=F('opponent_score')).count()
    losses = games.filter(team_score__lt=F('opponent_score')).count()
    ties = games.filter(team_score=F('opponent_score')).count() #will remove later to space for over time

    # quarter analysis
    quarters = {
        'q1_avg': games.aggregate(avg=Avg('q1_team'))['avg'] or 0,
        'q2_avg': games.aggregate(avg=Avg('q2_team'))['avg'] or 0,
        'q3_avg': games.aggregate(avg=Avg('q3_team'))['avg'] or 0,
        'q4_avg': games.aggregate(avg=Avg('q4_team'))['avg'] or 0,
    }

    # find best quarter
    best_quarter = max(quarters, key=quarters.get)

    return {
        'total_games': games.count(),
        'record': {
            'wins': wins,
            'losses': losses,
            'ties': ties,
            'win_percentage': round((wins / games.count() * 100) if games.count() > 0 else 0, 1)
        },
        'averages': {
            'points_scored': round(avg_points, 1),
            'points_allowed': round(avg_allowed, 1),
            'margin': round(avg_points - avg_allowed, 1)
        },
        'best_game': {
            'date': best_game.game_date if best_game else None,
            'score': f"{best_game.team_score}-{best_game.opponent_score}" if best_game else None
        } if best_game else None,
        'worst_game': {
            'date': worst_game.game_date if worst_game else None,
            'score': f"{worst_game.team_score}-{worst_game.opponent_score}" if worst_game else None
        } if worst_game else None,
        'quarter_analysis': {
            'q1_avg': round(quarters['q1_avg'], 1),
            'q2_avg': round(quarters['q2_avg'], 1),
            'q3_avg': round(quarters['q3_avg'], 1),
            'q4_avg': round(quarters['q4_avg'], 1),
            'best_quarter': best_quarter.replace('_avg', '').upper()
        }
    }