from django.db import models
from django.conf import settings
import secrets # more secure than random

def generate_join_code():
    # opted for manual assignment to lower chances of confusion like letter l and I.
    alphabet = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    # loops through alphabet, picks randomly and joins the list to form one string
    return ''.join(secrets.choice(alphabet) for _ in range(8))

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Team Name")

    join_code = models.CharField(
        max_length=20,
        unique=True,
        default=generate_join_code,
        editable=False,
        verbose_name="Join Code"
    )

    description = models.TextField(blank=True, verbose_name="Team Description")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, # incase of update, you only change from settings.py
        on_delete=models.CASCADE, # sought of like a chain reaction
        related_name='owned_teams',
        verbose_name="Created By"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    is_active = models.BooleanField(default=True, verbose_name="Active")

    # Probably you don't want someone having or knowing the code
    def regenerate_join_code(self):
        self.join_code = generate_join_code()
        self.save()

    def __str__(self):
        return f"{self.name} (Code: {self.join_code})"

    class Meta:
        db_table = 'team' #what shows up in the database
        ordering = ['-created_at'] # order of display
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['join_code']),
            models.Index(fields=['created_by']),
        ]

# apps/teams/models.py (add this after Team model)

class TeamMember(models.Model):
    ROLE_CHOICES = (
        ('COACH', 'Coach/Admin'),
        ('PLAYER', 'Player'),
    )

    POSITION_CHOICES = (
        ('PG', 'Point Guard'),
        ('SG', 'Shooting Guard'),
        ('SF', 'Small Forward'),
        ('PF', 'Power Forward'),
        ('C', 'Center'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='team_memberships',
        verbose_name="User"
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name="Team"
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='PLAYER',
        verbose_name="Team Role"
    )

    position = models.CharField(
        max_length=2,
        choices=POSITION_CHOICES,
        blank=True,
        null=True,
        verbose_name="Position"
    )

    jersey_number = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="Jersey Number"
    )

    is_active = models.BooleanField(default=True, verbose_name="Active Member")

    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Joined At"
    )

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"

    class Meta:
        db_table = 'team_member'
        unique_together = ['user', 'team']  # One membership per user per team
        ordering = ['joined_at']
        indexes = [
            models.Index(fields=['user', 'team']),
            models.Index(fields=['team']),
            models.Index(fields=['user']),
        ]

