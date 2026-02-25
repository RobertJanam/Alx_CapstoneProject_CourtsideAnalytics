from django.test import TestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.teams.models import Team, TeamMember
from .models import Game, PlayerStat
from datetime import date

# Create your tests here.
User = get_user_model()

class GameTests(TestCase):
    """Test game creation and statistics"""
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.coach = User.objects.create_user(
            username='coach',
            email='coach@example.com',
            password='testpass123'
        )

        self.player = User.objects.create_user(
            username='player',
            email='player@example.com',
            password='testpass123'
        )

        # Create team
        self.team = Team.objects.create(
            name='Test Team',
            created_by=self.coach
        )

        # Add members
        self.coach_member = TeamMember.objects.create(
            user=self.coach,
            team=self.team,
            role='COACH'
        )

        self.player_member = TeamMember.objects.create(
            user=self.player,
            team=self.team,
            role='PLAYER'
        )

        # Login as coach
        login_response = self.client.post('/api/auth/login/', {
            'email': 'coach@example.com',
            'password': 'testpass123'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.games_url = f'/api/teams/{self.team.id}/games/'

    def test_create_game(self):
        """Test that coach can create a game"""
        data = {
            'opponent_name': 'Opponent Team',
            'game_date': str(date.today()),
            'team_score': 75,
            'opponent_score': 70,
            'q1_team': 20,
            'q1_opponent': 15,
            'q2_team': 18,
            'q2_opponent': 20,
            'q3_team': 22,
            'q3_opponent': 18,
            'q4_team': 15,
            'q4_opponent': 17
        }
        response = self.client.post(self.games_url, data, format='json')
        print('Create Game Response Status:', response.status_code)
        print('Create Game Response Data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 1)

        # Check winner calculation
        game = Game.objects.first()
        self.assertEqual(game.winner, 'Test Team')
        self.assertEqual(game.margin, 5)

    def test_player_cannot_create_game(self):
        """Test that players cannot create games"""
        # Login as player
        login_response = self.client.post('/api/auth/login/', {
            'email': 'player@example.com',
            'password': 'testpass123'
        }, format='json')
        player_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {player_token}')

        data = {
            'opponent_name': 'Opponent Team',
            'game_date': str(date.today()),
            'team_score': 75,
            'opponent_score': 70,
            'q1_team': 20,
            'q1_opponent': 15,
            'q2_team': 18,
            'q2_opponent': 20,
            'q3_team': 22,
            'q3_opponent': 18,
            'q4_team': 15,
            'q4_opponent': 17
        }
        response = self.client.post(self.games_url, data, format='json')
        print('Player Cannot Create Game Response Status:', response.status_code)
        print('Player Cannot Create Game Response Data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)