from django.test import TestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Team, TeamMember

# Create your tests here.
# majority of the code is provided by AI
User = get_user_model()

class TeamTests(TestCase):
    """Test team creation and membership"""

    def setUp(self):
        self.client = APIClient()

        # Create a user
        self.user = User.objects.create_user(
            username='coach',
            email='coach@example.com',
            password='testpass123'
        )

        # Create another user for testing joins
        self.player = User.objects.create_user(
            username='player',
            email='player@example.com',
            password='testpass123'
        )

        # Login and get token
        login_response = self.client.post('/api/auth/login/', {
            'email': 'coach@example.com',
            'password': 'testpass123'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.teams_url = '/api/teams/'
        self.join_url = '/api/teams/join/'

    def test_create_team(self):
        """Test that a user can create a team"""
        data = {
            'name': 'Test Team',
            'description': 'A team for testing'
        }
        response = self.client.post(self.teams_url, data, format='json')
        print('Create Team Response Status:', response.status_code)
        print('Create Team Response Data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)

        # Check that creator became coach
        team = Team.objects.first()
        self.assertTrue(TeamMember.objects.filter(
            user=self.user,
            team=team,
            role='COACH'
        ).exists())

    def test_list_teams(self):
        """Test that user can list their teams"""
        # Create a team first
        team = Team.objects.create(
            name='My Team',
            created_by=self.user
        )
        TeamMember.objects.create(
            user=self.user,
            team=team,
            role='COACH'
        )

        response = self.client.get(self.teams_url)
        print('List Teams Response Status:', response.status_code)
        print('List Teams Response Data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'My Team')

    def test_join_team_with_code(self):
        """Test that a player can join a team with code"""
        # Coach creates team
        team = Team.objects.create(
            name='Joinable Team',
            created_by=self.user
        )
        TeamMember.objects.create(
            user=self.user,
            team=team,
            role='COACH'
        )

        # Switch to player account
        login_response = self.client.post('/api/auth/login/', {
            'email': 'player@example.com',
            'password': 'testpass123'
        }, format='json')
        player_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {player_token}')

        # Player joins with code
        data = {'join_code': team.join_code}
        response = self.client.post(self.join_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check membership created
        self.assertTrue(TeamMember.objects.filter(
            user=self.player,
            team=team,
            role='PLAYER'
        ).exists())

    def test_join_team_invalid_code(self):
        """Test joining with invalid code fails"""
        data = {'join_code': 'invalidcode'}
        response = self.client.post(self.join_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)