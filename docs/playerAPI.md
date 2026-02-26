### playerAPI
Handles specific performance data (box scores) for players within a game.

```markdown
# Player Statistics API

**Base URL:** `http://127.0.0.1:8000/api/games/`
**Headers:** `Authorization: Bearer <access_token>`

---

## Add Player Stats (Coaches only)
Submit performance data for a player in a specific game.
* **Endpoint:** `POST /{game_id}/stats/add/`

**Request Body:**
**Success Response (200 OK)**
```json
{
    "user": 1,
    "player": 1,
    "game": 1,
    "minutes_played": "28",
    "points": 27,
    "assists": 3,
    "rebounds": 8,
    "steals": 1,
    "blocks": 4,
    "turnovers": 2,
    "fouls": 5,
    "field_goals_made": 10,
    "field_goals_attempted": 17,
    "three_points_made": 2,
    "three_points_attempted": 2,
    "free_throws_made": 1,
    "free_throws_attempted": 2
}
```

---

# View player stats

* **Endpoint:** GET `/{game_id}/stats/`

**Request Body:**
**Success Response (200 OK)**

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "player_name": "johndoe",
            "player_position": "SF",
            "field_goal_pct": 60.0,
            "three_point_pct": 30.0,
            "free_throw_pct": 0.0,
            "efficiency_rating": 25,
            "minutes_played": 27,
            "points": 21,
            "assists": 4,
            "rebounds": 3,
            "steals": 1,
            "blocks": 0,
            "turnovers": 3,
            "fouls": 1,
            "field_goals_made": 9,
            "field_goals_attempted": 14,
            "three_points_made": 1,
            "three_points_attempted": 3,
            "free_throws_made": 0,
            "free_throws_attempted": 0,
            "recorded_at": "2026-02-26T11:23:15.279645Z",
            "game": 1,
            "player": 1
        },
        {
            "id": 2,
            "player_name": "TimDuncan",
            "player_position": "C",
            "field_goal_pct": 60.0,
            "three_point_pct": 100.0,
            "free_throw_pct": 50.0,
            "efficiency_rating": 36,
            "minutes_played": 28,
            "points": 27,
            "assists": 3,
            "rebounds": 8,
            "steals": 1,
            "blocks": 4,
            "turnovers": 2,
            "fouls": 5,
            "field_goals_made": 10,
            "field_goals_attempted": 17,
            "three_points_made": 2,
            "three_points_attempted": 2,
            "free_throws_made": 1,
            "free_throws_attempted": 2,
            "recorded_at": "2026-02-26T07:48:55.376392Z",
            "game": 1,
            "player": 2
        }
    ]
}
```