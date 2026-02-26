# Basketball Courtside Analytics API Documentation

**Base URL:** `http://127.0.0.1:8000/api/`

**Authentication:** JWT (JSON Web Tokens)

- All endpoints except registration and login require a valid access token
- Include token in request header: `Authorization: Bearer <your_access_token>`

**DOCUMENTATION**

- *authAPI.md*
- *userAPI.md*
- *teamAPI.md*
- *gameAPI.md*
- *analyticAPI.md*

**Testing with Postman**

*Setup Instructions:*
- Create a new collection in Postman

- Set up environment variables:

- base_url = http://127.0.0.1:8000/api
- access_token = (will be populated after login)

*Test Flow:*

- First: POST /auth/register/ to create a user

- Then: POST /auth/login/ to get tokens

- Copy the access_token to your environment

- All subsequent requests need header:

- Authorization: Bearer {{access_token}}

*Sample Test Sequence:*

1. Register coach

2. Login -> get token

3. Create team

4. Register player (new user)

5. Login as player -> get token

6. Player joins team with code

7. Coach creates game

8. Coach adds player stats

9. View analytics