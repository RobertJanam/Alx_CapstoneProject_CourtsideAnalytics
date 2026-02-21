from rest_framework import serializers
from .models import Game, PlayerStat

class PlayerStatSerializer(serializers.ModelSerializer):
    # readable player info
    player_name = serializers.CharField(source='player.user.username', read_only=True)

    player_position = serializers.CharField(source='player.position', read_only=True)

    # calculated fields from model properties
    # source points to the property method in the model
    field_goal_pct = serializers.FloatField(source='field_goal_percentage', read_only=True)

    three_point_pct = serializers.FloatField(source='three_point_percentage', read_only=True)

    free_throw_pct = serializers.FloatField(source='free_throw_percentage', read_only=True)

    efficiency_rating = serializers.IntegerField(source='efficiency', read_only=True)

    class Meta:
        model = PlayerStat
        # '__all__' includes all model fields
        # plus our custom fields above
        fields = '__all__'
        read_only_fields = ['id', 'recorded_at']

    def validate_minutes_played(self, value):
        # minutes played must be reasonable
        if value < 0 or value > 48:
            raise serializers.ValidationError(
                "Minutes played must be between 0 and 48."
            )
        return value

    def validate(self, data):
        # Check field goals: eg. field goal made cannot be > field goals attempted
        if data.get('field_goals_made', 0) > data.get('field_goals_attempted', 0):
            raise serializers.ValidationError({
                'field_goals_made': "Field goals made cannot exceed attempts."
            })

        # Check three pointers
        if data.get('three_points_made', 0) > data.get('three_points_attempted', 0):
            raise serializers.ValidationError({
                'three_points_made': "Three pointers made cannot exceed attempts."
            })

        # Check free throws
        if data.get('free_throws_made', 0) > data.get('free_throws_attempted', 0):
            raise serializers.ValidationError({
                'free_throws_made': "Free throws made cannot exceed attempts."
            })

        return data


class GameSerializer(serializers.ModelSerializer):
    # used for game listings

    # computed fields from model properties
    team_name = serializers.CharField( source='team.name', read_only=True)

    winner = serializers.CharField(read_only=True  # from model property
    )

    margin = serializers.IntegerField(read_only=True  # from model property
    )

    class Meta:
        model = Game
        fields = [
            'id',
            'team',
            'team_name',
            'opponent_name',
            'game_date',
            'venue',
            'team_score',
            'opponent_score',
            'winner',          # logic handled
            'margin',          # logic handled
            'q1_team', 'q1_opponent',
            'q2_team', 'q2_opponent',
            'q3_team', 'q3_opponent',
            'q4_team', 'q4_opponent',
            'notes',
            'recorded_by',
            'recorded_at'
        ]
        read_only_fields = ['id', 'recorded_at', 'recorded_by']

    def validate(self, data):
        # ensure quarter scores add up to final score
        # sum all quarter scores
        total_q_team = (
            data.get('q1_team', 0) +
            data.get('q2_team', 0) +
            data.get('q3_team', 0) +
            data.get('q4_team', 0)
        )

        total_q_opponent = (
            data.get('q1_opponent', 0) +
            data.get('q2_opponent', 0) +
            data.get('q3_opponent', 0) +
            data.get('q4_opponent', 0)
        )

        # Check if totals match final scores
        if 'team_score' in data and total_q_team != data['team_score']:
            raise serializers.ValidationError({
                'team_score': f"Quarter scores sum to {total_q_team}, but final score is {data['team_score']}"
            })

        if 'opponent_score' in data and total_q_opponent != data['opponent_score']:
            raise serializers.ValidationError({
                'opponent_score': f"Quarter scores sum to {total_q_opponent}, but final score is {data['opponent_score']}"
            })

        return data


class GameDetailSerializer(serializers.ModelSerializer):
    # used for single game views.

    team_name = serializers.CharField(source='team.name', read_only=True)

    # include all player stats for this game
    player_stats = PlayerStatSerializer(
        many=True,        #one game has many player stats
        read_only=True    #can't modify stats through game serializer
    )

    winner = serializers.CharField(read_only=True)
    margin = serializers.IntegerField(read_only=True)

    class Meta:
        model = Game
        fields = '__all__'  # includes everything, plus player_stats