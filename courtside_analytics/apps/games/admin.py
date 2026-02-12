from django.contrib import admin
from .models import Game, PlayerStat
# Register your models here.

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('team', 'opponent_name', 'game_date', 'team_score', 'opponent_score')
    list_filter = ('game_date', 'team')
    search_fields = ('team__name', 'opponent_name')

@admin.register(PlayerStat)
class PlayerStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'game', 'points', 'assists', 'rebounds')
    list_filter = ('game__game_date',)
    search_fields = ('player__user__username', 'game__opponent_name')