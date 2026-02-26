# Team Management API
Handles team creation, joining via codes, and roster management.

**Base URL:** `http://127.0.0.1:8000/api/teams/`
**Headers:** `Authorization: Bearer <access_token>`

---

### List & Create Teams
* **GET `/`**: Returns all teams the user belongs to.
* **POST `/`**: Create a new team.

**Create Request Body:**
```json
{
    "name": "Kisumu Bucks",
    "description": "Community basketball team"
}
```

---
### Join Team

* **Endpoint:** POST `/join/`

**Request Body:**

```json
{ "join_code": "aB3xK9mP" }
```

**Success Response (201 Created):**

```json
{
    "message": "Successfully joined Nairobi Lions",
    "team": {
        "id": 1,
        "name": "Nairobi Lions",
        "join_code": "aB3xK9mP",
        "members_count": 2
    },
    "role": "PLAYER"
}
```

**Error Responses:**
* **400 Bad Request:** Invalid join code
* **400 Bad Request:** Already a member of this team

*Already a member?*
**Request Body:**

```json
{
    "error": "You are already a member of this team."
}
```

---

### Update team info (Coaches only)
* **Endpoint:** PUT `/{id}/`

**Request Body:**

```json
{
    "name": "Nairobi Lions Elite",
    "description": "Updated team description"
}
```

* **Success Response (200 OK):** Returns updated team object

**Error Responses:**
* **403 Forbidden:** User is not a coach of this team
* **404 Not Found:** Team doesn't exist

---

### Delete team: Soft delete (Coaches only)
* **Endpoint:** DELETE `/{id}/`
* **Success Response:** 204 No Content

---

## Roster Management

### List members: players/coaches
* **Endpoint:** GET `/{team_id}/members/`

**Response Body:**

```json

{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": 1,
            "user_details": {
                "id": 1,
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "phone_number": "0712345678",
                "date_joined": "date joined"
            },
            "role": "PLAYER",
            "position": "SG",
            "jersey_number": 10,
            "is_active": true,
            "joined_at": "date joined"
        },
        {
            "id": 2,
            "user": 2,
            "user_details": {
                "id": 2,
                "username": "TimDuncan",
                "email": "timduncan@gmail.com",
                "phone_number": null,
                "date_joined": "2026-02-21T11:31:30.426498Z"
            },
            "role": "PLAYER",
            "position": "C",
            "jersey_number": 5,
            "is_active": true,
            "joined_at": "2026-02-21T11:33:16.164741Z"
        }
    ]
}
```

---

### Update members for team (Coaches only)
* **Endpoint:** PUT `/{team_id}/members/{member_id}/`

*Available position options:* PG, SG, SF, C

*Position constraint:* Unique for every member


*Default*
```json
{
    "user": 1,
    "position": null,
    "jersey": null
}
```

**Request Body:**

```json
{
    "user": 1,
    "position": "C",
    "jersey": "5"
}
```

**Success Response (200 OK):**

```json
{
    "id": 2,
    "user": 2,
    "username": "TimDuncan",
    "role": "PLAYER",
    "position": "C",
    "jersey_number": 23,
    "is_active": true,
    "joined_at": "2026-02-25T11:30:00Z"
}
```

* **Response Body:** Not coach

```json
{
    "detail": "You do not have permission to perform this action."
}
```

---

### Remove member (Coaches only)
* **Endpoint:** DELETE `/{team_id}/members/{member_id}/`

**Success Response:**

* **Status:** 204 No Content

* **Body:** Empty