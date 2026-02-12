from django.contrib import admin
from .models import Team, TeamMember

# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'join_code', 'created_by', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'join_code')
    readonly_fields = ('join_code',) #must not be allowed to change
    actions = ['regenerate_join_codes']

    def regenerate_join_codes(self, request, queryset):
        for team in queryset:
            team.regenerate_join_code()
        self.message_user(request, f"{queryset.count()} teams' join codes regenerated.")
    regenerate_join_codes.short_description = "Regenerate join codes for selected teams"

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'position', 'jersey_number', 'joined_at')
    list_filter = ('position', 'team')
    search_fields = ('user__username', 'team__name')