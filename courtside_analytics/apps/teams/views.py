from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Team, TeamMember
from .serializers import (
    TeamSerializer,
    TeamMemberSerializer,
    TeamDetailSerializer,
    JoinTeamSerializer
)


# Create your views here.
class TeamListView(generics.ListCreateAPIView):
    # this is an API endpoint for listing user's teams and creating new teams
    # GET/api/teams/ will list all teams the current user belongs to
    # POST/api/teams/ will create new team. (the current user will be the coach)

    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # get the current user team (filter)

        # get all team IDs where current user is a member
        user_team_ids = TeamMember.objects.filter(
        user=self.request.user,
        is_active=True).values_list('team_id', flat=True)

        return Team.objects.filter(id__in=user_team_ids, is_active=True)

    def perform_create(self, serializer):
        # when creating a team, save the team with current user as the creator
        # and automatically create TeamMember entry with role=COACH

        team = serializer.save(created_by=self.request.user)

        TeamMember.objects.create(
            user=self.request.user,
            team=team,
            role="COACH"
        )


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    # This is an API endpoint for retrieving, updating and deleting a specific team
    # GET/api/teams/{id}/: view team details
    # PUT/api/teams/{id}/: update team (only for coaches)
    # DELETE/api/teams/{id}: delete team (only for coaches)


    def get_serializer_class(self):
        if self.request.method == "GET":
            return TeamDetailSerializer # with members
        return TeamSerializer # basic version (for updates)

    def get_queryset(self):
        # all active teams
        return Team.objects.filter(is_active=True)

    def get_object(self):
        # get team and then verify if user has permission
        team = super().get_object()

        # check if the user is a member of this team
        if not TeamMember.objects.filter(
            user=self.request.user, team=team,
            is_active=True).exists():

            raise PermissionDenied("You are not a member of this team.")

        return team

    def perform_update(self, serializer):
        # allow only coaches to update
        team = self.get_object()

        # check if user is a coach of this team
        if not TeamMember.objects.filter(
            user=self.request.user, team=team,
            role="COACH").exists():

            raise PermissionDenied("Only team coaches can update team information.")
            serializer.save()

    def perform_destroy(self, instance):
        # delete team (but soft delete)
        instance.is_active = False
        instance.save()


class JoinTeamView(generics.CreateAPIView):
    # This is an API endpoint for joining a team using a join code
    # POST/api/teams/join/
    # Automatically create TeamMember with role as PLAYER

    serializer_class = JoinTeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get team from validated data
        team = serializer.validated_data['team']

        # check whether use is already a member or not
        if TeamMember.objects.filter(user=request.user,team=team).exists():
            return Response(
                {"error": "You are already a member of this team."},
                status=status.HTTP_400_BAD_REQUEST)

        # create membership
        member = TeamMember.objects.create(
            user=request.user,
            team=team,
            role="PLAYER" # role is PLAYER
        )

        return Response(
            {
                "message": f"Successfully joined {team.name}",
                "team" : TeamSerializer(team).data,
                "role": member.role
            },
            status=status.HTTP_201_CREATED
        )


class TeamMembersView(generics.ListAPIView):
    # API endpoint for listing all members of this team
    # GET/api/teams/{team_id}/members/
    # Only team members can view the member list

    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        team = get_object_or_404(Team, id=team_id)

        # Verify user is a member of the team
        if not TeamMember.objects.filter(
            user=self.request.user, team=team,
            is_active=True).exists():
            raise PermissionDenied("You are not a member of this team.")

        # return all members of this team (active ones)
        return TeamMember.objects.filter(
            team=team,
            is_active=True
        ).select_related('user') # load user data


class TeamMemberUpdateView(generics.UpdateAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        return TeamMember.objects.filter(team_id=team_id)

    def get_object(self):
        member_id = self.kwargs['member_id']
        return get_object_or_404(self.get_queryset(), id=member_id)

    def perform_update(self, serializer):
        team_member = self.get_object()
        team = team_member.team

        # only coaches can update member details
        if not TeamMember.objects.filter(user=self.request.user, team=team, role='COACH', is_active=True).exists():
            raise PermissionDenied("Only coaches can update team member details.")
        serializer.save()