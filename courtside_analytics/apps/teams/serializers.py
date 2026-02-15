from rest_framework import serializers
from .models import Team, TeamMember
from apps.users.serializers import UserSerializer # reuse


class TeamMemberSerializer(serializers.ModelSerializer):
    # shows membership info for a specific team

    # includes full user details
    # source tells it to get data from a field
    # read_only for allowing/disallowing modification

    user_details = UserSerializer(source='user', read_only=True)

    username = serializers.CharField(source='users.username', read_only=True)

    class Meta:
        model = ['id',
            'user',
            'username', # for reading
            'user_details',   # for reading
            'role',
            'position',
            'jersey_number',
            'is_active',
            'joined_at'
        ]

        read_only_fields=['id', 'joined_at', 'role']

        extra_kwargs = {
            'position': {'allow_null': True, 'required': False},
            'jersey_number': {'allow_null': True, 'required': False}
        }

    def validate_jersey_number(self, value):
        if value is not None:
            if (value < 0 or value > 99):
                raise serializers.ValidateError(
                    "Jersey number must be between 0 and 99."
                )

            # check if this jersey number is already taken in this team
            team = self.instance.team if self.instance else None
            if team and value:
                exists = TeamMember.objects.filter(team=team, jersey_number=value
                ).exclude(id=self.instance.id if self.instance else None).exists()

                if exists:
                    raise serializers.ValidationError(
                        f"Jersey number {value} is already taken in this team."
                    )

        return value


class TeamSerializer(serializers.ModelSerializer):

    #count member
    members_count = serializers.IntegerField(source='members.count', read_only=True)

    # show creator's username
    created_by_username = serializers.CharField(source='created_by.username')

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'join_code',
            'description',
            'created_by',
            'created_by_username',
            'created_at',
            'is_active',
            'members_count'
        ]
        read_only_fields = ['id', 'join_code', 'created_at', 'created_by']

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Team name must be at least 3 characters long."
            )

        return value


class TeamDetailSerializer(serializers.ModelSerializer):
    # includes full member list
    # used for individual team views

    #include all members with full names
    members = TeamMemberSerializer(many=True, read_only=True)

    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        fields = [
            'id',
            'name',
            'join_code',
            'description',
            'created_by',
            'created_by_username',
            'created_at',
            'is_active',
            'members'
        ]
        read_only_fields = ['id', 'join_code', 'created_at', 'created_by']


class JoinTeamSerializer(serializers.Serializer):
    # for joining a team with a code
    # validates the join code

    join_code = serializers.CharField(
        max_length=20,
        help_text="The 8-character team join code",
        write_only=True
    )

    def validate_join_code(self, value):
        try:
            team = Team.objects.get(join_code=value, is_active=True)
        except Team.DoesNotExist:
            raise serializers.ValidationError(
            "Invalid join code. Please check and try again."
            )

        return value

    def validate(self, data):
        # after field validation, attach the team object to data
        # this makes it available in the view

        code = data.get("join_code")
        team = Team.objects.get(join_code=code, is_active=True)
        data['Team'] = team

        return data