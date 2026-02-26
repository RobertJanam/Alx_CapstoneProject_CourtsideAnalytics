# Games API
Manages game records, quarterly scores, and results.

**Base URL:** `http://127.0.0.1:8000/api/`
**Headers:** `Authorization: Bearer <access_token>`

---

## Team Game Records

### Create a new game record
* **Endpoint:** POST `/teams/{team_id}/games/`

**Success Response(200 OK)**
**Request Body:**

```json
{
    "team": 1,
    "opponent_name": "Mombasa Sharks",
    "game_date": "2026-02-25",
    "venue": "Sports Ground",
    "team_score": 78,
    "opponent_score": 65,
    "q1_team": 17, "q1_opponent": 13,
    "q2_team": 15, "q2_opponent": 20,
    "q3_team": 25, "q3_opponent": 17,
    "q4_team": 21, "q4_opponent": 15
}
```

---

### List all games for a team
* **Endpoint:** GET `/teams/{team_id}/games/`

**Success Response (200 OK)**
**Response Body:**

```json

{
"count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "team": 1,
            "team_name": "Kisumu Bucks",
            "opponent_name": "Mombasa Sharks",
            "game_date": "2026-02-25",
            "venue": "Sports Ground",
            "team_score": 78,
            "opponent_score": 65,
            "winner": "Kisumu Bucks",
            "margin": 13,
            "q1_team": 17,
            "q1_opponent": 13,
            "q2_team": 15,
            "q2_opponent": 20,
            "q3_team": 25,
            "q3_opponent": 17,
            "q4_team": 21,
            "q4_opponent": 15,
            "notes": "",
            "recorded_by": 1,
            "recorded_at": "2026-02-26T09:01:00.337027Z"
        }
    ]
}
```

---

### Fetch full game details, including player stats
* **Endpoint:** GET `/games/{id}/`

**Success Response (200 OK)**
**Response Body:**
```json

{
    "id": 1,
    "team_name": "Kisumu Bucks",
    "player_stats": [
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
            "recorded_at": "2026-02-25T11:23:15.279645Z",
            "game": 1,
            "player": 2
        },
        {
            "id": 3,
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
            "recorded_at": "2026-02-25T07:48:55.376392Z",
            "game": 1,
            "player": 1
        }
    ],
    "winner": "Kisumu Bucks",
    "margin": 13,
    "opponent_name": "Mombasa Sharks",
    "game_date": "2026-02-25",
    "venue": "Sports Ground",
    "team_score": 78,
    "opponent_score": 65,
    "q1_team": 17,
    "q1_opponent": 13,
    "q2_team": 15,
    "q2_opponent": 20,
    "q3_team": 25,
    "q3_opponent": 17,
    "q4_team": 21,
    "q4_opponent": 15,
    "recorded_at": "2026-02-21T09:01:00.337027Z",
    "notes": "",
    "team": 1,
    "recorded_by": 1
}
```

---

### Update game info (Coaches Only)

* **Endpoint:** PUT `/games/{id}/`

**Success Response (200 OK)**
**Request Body:**

```json
{
    "team": 2,
    "opponent_name": "Kisumu Raiders",
    "game_date": "2026-02-26",
    "team_score": 78,
    "opponent_score": 65,
    "q1_team": 17,
    "q1_opponent": 13,
    "q2_team": 15,
    "q2_opponent": 20,
    "q3_team": 25,
    "q3_opponent": 17,
    "q4_team": 21,
    "q4_opponent":15
}
```

---

### Remove game (Coaches only)
* **Endpoint:** DELETE `/games/{id}/`

**Success Response:**

* **Status:** 204 No Content
* **Body:** Empty