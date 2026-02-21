from django.db import models
from apps.teams.models import Team, TeamMember
from django.conf import settings

# Create your models here.
class Game(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='games',
        verbose_name="Team"
    )

    opponent_name = models.CharField(max_length=100, verbose_name="Opponent Name"
    )

    game_date = models.DateField(verbose_name="Game Date")

    venue = models.CharField(max_length=200, blank=True, verbose_name="Venue"
    )

    # Final scores
    team_score = models.IntegerField(verbose_name="Team Score")

    opponent_score = models.IntegerField(verbose_name="Opponent Score")

    # Quarter scores (null for games that don't track quarter scores)
    q1_team = models.IntegerField(default=0, verbose_name="Q1 Team Score")

    q1_opponent = models.IntegerField(default=0, verbose_name="Q1 Opponent Score")

    q2_team = models.IntegerField(default=0, verbose_name="Q2 Team Score")

    q2_opponent = models.IntegerField(default=0, verbose_name="Q2 Opponent Score")

    q3_team = models.IntegerField(default=0, verbose_name="Q3 Team Score")

    q3_opponent = models.IntegerField(default=0, verbose_name="Q3 Opponent Score")

    q4_team = models.IntegerField(default=0, verbose_name="Q4 Team Score")

    q4_opponent = models.IntegerField(default=0, verbose_name="Q4 Opponent Score")

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='recorded_games',
        verbose_name="Recorded By"
    )

    recorded_at = models.DateTimeField(auto_now_add=True, verbose_name="Recorded At")

    notes = models.TextField(blank=True, verbose_name="Game Notes")

    @property # because this is calculated and not stored
    def winner(self):
        if self.team_score > self.opponent_score:
            return self.team.name
        elif self.opponent_score > self.team_score:
            return self.opponent_name
        else:
            return "Tie" # later on add logic for over time

    @property
    # points differential
    def margin(self):
        return self.team_score - self.opponent_score

    def __str__(self):
        return f"{self.team.name} vs {self.opponent_name} - {self.game_date}"

    class Meta:
        db_table = 'game'
        ordering = ['-game_date']
        indexes = [
            models.Index(fields=['team', 'game_date']),
            models.Index(fields=['game_date']),
            models.Index(fields=['recorded_by']),
        ]

class PlayerStat(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='player_stats',
        verbose_name="Game"
    )

    player = models.ForeignKey(
        TeamMember,  # Direct to TeamMember, not CustomUser
        on_delete=models.CASCADE,
        related_name='game_stats',
        verbose_name="Player"
    )

    # Basic stats
    minutes_played = models.IntegerField(default=0, verbose_name="Minutes Played")

    points = models.IntegerField(default=0, verbose_name="Points")

    assists = models.IntegerField(default=0, verbose_name="Assists")

    rebounds = models.IntegerField(default=0, verbose_name="Rebounds")

    steals = models.IntegerField(default=0, verbose_name="Steals")

    blocks = models.IntegerField(default=0, verbose_name="Blocks")

    turnovers = models.IntegerField(default=0, verbose_name="Turnovers")

    fouls = models.IntegerField(default=0, verbose_name="Fouls")

    # advanced shooting stats
    field_goals_made = models.IntegerField(default=0, verbose_name="Field Goals Made")

    field_goals_attempted = models.IntegerField(default=0, verbose_name="Field Goals Attempted")

    three_points_made = models.IntegerField(default=0, verbose_name="3-Pointers Made")

    three_points_attempted = models.IntegerField(default=0, verbose_name="3-Pointers Attempted")

    free_throws_made = models.IntegerField(default=0, verbose_name="Free Throws Made")

    free_throws_attempted = models.IntegerField(default=0, verbose_name="Free Throws Attempted")

    recorded_at = models.DateTimeField(auto_now_add=True, verbose_name="Recorded At")

    @property
    def field_goal_percentage(self):
        if self.field_goals_attempted > 0:
            return round(self.field_goals_made / self.field_goals_attempted, 1) * 100
        return 0.0

    @property
    def three_point_percentage(self):
        if self.three_points_attempted > 0:
            return round(self.three_points_made / self.three_points_attempted, 1) * 100
        return 0.0

    @property
    def free_throw_percentage(self):
        if self.free_throws_attempted > 0:
            return round(self.free_throws_made / self.free_throws_attempted, 1) * 100
        return 0.0

    @property
    def efficiency(self):
        return (self.points + self.rebounds + self.assists +
                self.steals + self.blocks) - (self.turnovers + self.fouls)

    def __str__(self):
        return f"{self.player.user.username} - {self.game} - {self.points} pts"

    class Meta:
        db_table = 'player_stat'
        unique_together = ['game', 'player']
        ordering = ['-game__game_date']
        indexes = [
            models.Index(fields=['player', 'game']),
            models.Index(fields=['game']),
            models.Index(fields=['player']),
            models.Index(fields=['points']),
        ]