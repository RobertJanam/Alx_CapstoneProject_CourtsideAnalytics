### analyticAPI
Aggregated data and performance trends.

```markdown
# Analytics API

**Base URL:** `http://127.0.0.1:8000/api/analytics/`
**Headers:** `Authorization: Bearer <access_token>`

---

## Player Averages
* **Endpoint:** `GET /players/{player_id}/?team_id={id}`
* **Returns:** PPG, APG, RPG, SPG, BPG and total points.

**Response Body:**
**Success Response (200 OK)**

```json

{
    "games_played": 1,
    "ppg": 21.0,
    "apg": 4.0,
    "rpg": 3.0,
    "spg": 1.0,
    "bpg": 0,
    "total_points": 21
}
```

---

## Team Leaderboard
Rank players within a team.
* **Endpoint:** `GET /teams/{team_id}/leaderboard/`
* **Endpoint:** `GET /teams/{team_id}/leaderboard/?limit=number`
* **Query Params:** 'limit`, `team`, `ppg`, `ast`, `rbd`...

**Response Body:**
**Success Response (200 OK)**

```json

{
    "team": "Kisumu Bucks",
    "ppg": "points",
    "ast": "assists",
    "rbd": "rebounds",
    "stl": "steals",
    "blc": "blocks",
    "leaderboard": [
        {
            "player_id": 2,
            "player_name": "TimDuncan",
            "position": "C",
            "jersey_number": 5,
            "avg_points": 27.0,
            "avg_assists": 3.0,
            "avg_rebounds": 8.0,
            "avg_steals": 1.0,
            "avg_blocks": 4.0,
            "total_points": 27,
            "total_assists": 3,
            "total_rebounds": 8,
            "total_steals": 1,
            "total_blocks": 4,
            "games_played": 1
        },
        {
            "player_id": 1,
            "player_name": "johndoe",
            "position": "SF",
            "jersey_number": 10,
            "avg_points": 21.0,
            "avg_assists": 4.0,
            "avg_rebounds": 3.0,
            "avg_steals": 1.0,
            "avg_blocks": 0,
            "total_points": 21,
            "total_assists": 4,
            "total_rebounds": 3,
            "total_steals": 1,
            "total_blocks": 0,
            "games_played": 1
        }
    ]
}
```

---

## Team Trends
* **Endpoint:** `GET /teams/{team_id}/trends/`
* **Insight:** Includes win percentage, margin of victory, and quarter-by-quarter analysis.

**Response Body:**
**Success Response (200 OK)**

```json

{
    "total_games": 1,
    "record": {
        "wins": 1,
        "losses": 0,
        "ties": 0,
        "win_percentage": 100.0
    },
    "averages": {
        "points_scored": 78.0,
        "points_allowed": 65.0,
        "margin": 13.0
    },
    "best_game": {
        "date": "2026-02-26",
        "score": "78-65"
    },
    "worst_game": {
        "date": "2026-02-26",
        "score": "78-65"
    },
    "quarter_analysis": {
        "q1_avg": 17.0,
        "q2_avg": 15.0,
        "q3_avg": 25.0,
        "q4_avg": 21.0,
        "best_quarter": "Q3"
    },
    "team": "Kisumu Bucks"
}
```

---

## Game Analytics
* **Endpoint:** `GET /games/{game_id}/`
* **Insight:** Team totals vs. individual top scorers.

**Response Body:**
**Success Response (200 OK)**

```json
{
    "game": {
        "id": 2,
        "date": "2026-02-26",
        "opponent": "Kisumu Raiders",
        "score": "78-65",
        "winner": "Kisumu Bucks",
        "margin": 13
    },
    "team_totals": {
        "points": 48,
        "assists": 7,
        "rebounds": 11,
        "steals": 2,
        "blocks": 4,
        "turnovers": 5,
        "fouls": 6
    },
    "top_scorer": {
        "player": "TimDuncan",
        "points": 27
    },
    "player_stats": [
        {
            "player": "johndoe",
            "position": "SF",
            "points": 21,
            "assists": 4,
            "rebounds": 3,
            "steals": 1,
            "blocks": 0,
            "efficiency": 25
        },
        {
            "player": "TimDuncan",
            "position": "C",
            "points": 27,
            "assists": 3,
            "rebounds": 8,
            "steals": 1,
            "blocks": 4,
            "efficiency": 36
        }
    ]
}
```