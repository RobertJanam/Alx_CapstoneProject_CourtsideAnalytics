# Authentication API

Handle user registration and JWT token generation.

**Base URL:** `http://127.0.0.1:8000/api/auth/`

---

## Register New User
Creates a new account.
* **Endpoint:** POST `/register/`
* **Auth Required:** No

**Request Body:**
| Field | Type | Description |
| :--- | :--- | :--- |
| `username` | String | Unique username for the coach/player. |
| `email` | String | Valid email address. |
| `password` | String | Account password. |
| `password2` | String | Must match password. |
| `phone_number` | String | User contact info. |

**Success Response (201 Created):**
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
* **400 Bad Request:** Password mismatch or email already exists
* **400 Bad Request:** Missing required fields

---
## Login

* **Endpoint:** POST `/login/`
* **Auth Required:** No

**Request Body:**
| Field | Type | Description |
| :--- | :--- | :--- |
| `email` | String | Valid email address. |
| `password` | String | Account password. |

**Success Response (200 OK):**

```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@gmail.com",
        "phone_number": "",
        "date_joined": "date joined"
    }
}
```

**Error Responses:**
* **400 Bad Request:** Invalid credentials
* **400 Bad Request:** Missing email or password