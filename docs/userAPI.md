# User Profile API
Manages the authenticated user's profile and settings.

**Base URL:** `http://127.0.0.1:8000/api/auth/`
**Headers:** `Authorization: Bearer <access_token>`

---

## Get Current User Profile
Fetch details of the logged-in user.
Returns the authenticated user's profile.
* **Endpoint:** GET `/me/`

**Success Response (200 OK):**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@gmail.com",
    "phone_number": "",
    "date_joined": "date joined"
}
```

**Error Responses:**
* **401 Unauthorized:** Missing or invalid token

---

## Update Profile

* **Endpoint:** PUT `/me/` (Full Update) or PATCH `/me/` (Partial Update)

* **Sample Request (PATCH):**

```json
{
    "phone_number": "0723456789"
}
```

**Success Response (200 OK):**

```json
{
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@gmail.com",
    "phone_number": "0723456789",
    "date_joined": "date joined"
}
```