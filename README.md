# Basketball Courtside Analytics & Tracker API

[![Django](https://img.shields.io/badge/Django-6.0.2-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.16.1-red?style=for-the-badge&logo=django)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.12.12-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql)](https://www.mysql.com/)
[![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=json-web-tokens)](https://jwt.io/)

## 📋 Table of Contents
- [Project Description](#-project-description)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Database Setup](#database-setup)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
  - [Authentication Endpoints](#authentication-endpoints)
  - [User Profile Endpoints](#user-profile-endpoints)
  - [Team Management Endpoints](#team-management-endpoints)
  - [Game & Statistics Endpoints](#game--statistics-endpoints)
  - [Analytics Endpoints](#analytics-endpoints)
- [Testing](#-testing)
- [Architecture Overview](#-architecture-overview)
- [Project Structure](#-project-structure)
- [License](#-license)
- [Contributing](#-contributing)
- [Contact & Credits](#-contact--credits)

---

## Project Description

In Kenya, basketball leagues, especially at the grassroots level, struggle with game data tracking and analysis, often relying on physical paper records or basic spreadsheet tools that don't provide meaningful insights. Coaches need better tools to track player performance, analyze game trends, and make data-driven decisions.

**Basketball Courtside Analytics & Tracker** is a backend API built to solve this problem. It provides a platform for coaches and team staff to record game statistics, manage teams, and receive automated performance analytics.

The API focuses on making data entry simple while delivering powerful insights through calculated metrics like player averages, team leaderboards, and quarter-by-quarter performance trends.

---

## Features

### Core MVP Features
- **User Authentication System:** JWT-based registration and login.
- **Team Management:** Coaches can create teams (with unique join codes), players can join teams, and members can be managed.
- **Game Data Entry:** Coaches can record games with team scores, opponent scores, and quarter-by-quarter breakdowns.
- **Player Statistics:** Comprehensive stats tracking (points, assists, rebounds, steals, blocks, turnovers, fouls, shooting percentages) for each player per game.
- **Automated Analytics:**
  - Automatic win/loss determination and point differential.
  - Player averages (PPG, APG, RPG, SPG, BPG).
  - Team leaderboards for various stats.
  - Team performance trends, including quarter analysis and win percentage.

### Enhanced Features (Implemented)
- Multiple admin roles per team.
- Full CRUD operations for games and player stats (coach only).
- Soft delete functionality for teams and members.
- Role-based permissions (Coaches vs. Players).

---

## Technology Stack

| Category          | Technology                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------ |
| **Framework**     | [Django 6.0.2](https://www.djangoproject.com/) & [Django REST Framework 3.16.1](https://www.django-rest-framework.org/) |
| **Database**      | [MySQL 8.0](https://www.mysql.com/) (connected via MySQL Workbench 8.0 CE)                             |
| **Authentication**| [JWT](https://jwt.io/) (via `djangorestframework-simplejwt`)                                           |
| **API Docs**      | [Swagger UI](https://swagger.io/tools/swagger-ui/) & [ReDoc](https://github.com/Redocly/redoc) (via `drf-yasg`) |
| **Environment**   | Python 3.12.12, `venv`, `pip`                                                                          |
| **CORS**          | `django-cors-headers`                                                                                  |
| **Other Tools**   | `python-dotenv` for environment variables, Git for version control.                                    |

---

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed:
- **Python:** Version 3.12.12 (Recommended for `mysqlclient` compatibility).
- **MySQL:** Version 8.0 and MySQL Workbench 8.0 CE (or any MySQL client).
- **Git:** For cloning the repository.
- **Pip:** Python package installer (usually comes with Python).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Alx_CapstoneProject_CourtsideAnalytics.git
    cd Alx_CapstoneProject_CourtsideAnalytics
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # On Windows (PowerShell)
    python -m venv venv
    .\venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install django djangorestframework django-cors-headers djangorestframework-simplejwt
    pip install drf-yasg
    pip install mysqlclient
    pip install python-dotenv
    pip install -r requirements.txt
    ```

### Environment Variables

1.  Create a `.env` file in the project root directory (the same level as `manage.py`).
2.  Copy the contents from `.env.example` and fill in your values.

    ```env
    # .env.example
    # Django
    SECRET_KEY=your-super-secret-key-change-this-in-production
    DEBUG=True

    # Database
    DB_NAME=courtside_db
    DB_USER=root
    DB_PASSWORD=your_mysql_password
    DB_HOST=localhost
    DB_PORT=3306
    ```

    > **IMPORTANT:** Never commit your `.env` file to version control. It is already listed in `.gitignore`.

### Database Setup

1.  **Create the Database:** Open MySQL Workbench and create a new database schema. The name should match the `DB_NAME` in your `.env` file.
    ```sql
    CREATE DATABASE courtside_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```

2.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

3.  **Create a Superuser (Optional, for Django Admin):**
    ```bash
    python manage.py createsuperuser
    ```

4.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

The API will now be accessible at `http://127.0.0.1:8000/api/`. You can explore the interactive documentation at `http://127.0.0.1:8000/swagger/` or `http://127.0.0.1:8000/redoc/`.

---

## 📖 Usage

Once the server is running, you can interact with the API using tools like [Postman](https://www.postman.com/) or `curl`.

A typical workflow is:
1.  **Register** a new user (coach).
2.  **Login** to receive your JWT `access` token.
3.  Use this token in the `Authorization: Bearer <token>` header for all subsequent requests.
4.  **Create a team**.
5.  Have a player **register**, **login**, and **join** the team using the team's unique `join_code`.
6.  As a coach, **create a game** and then **add player statistics** for that game.
7.  Explore the **analytics endpoints** to see calculated averages and leaderboards.

A detailed Postman testing sequence is provided in the main `api.md` file.

---

## API Documentation

Comprehensive API documentation is available in both Markdown and interactive formats.

- **Interactive Docs:**
  - [Swagger UI](http://127.0.0.1:8000/swagger/) - `http://127.0.0.1:8000/swagger/`
  - [ReDoc](http://127.0.0.1:8000/redoc/) - `http://127.0.0.1:8000/redoc/`
- **Markdown Files:** Detailed breakdowns are located in the `docs/` directory (or root, based on your structure):
*   [Main API Overview](docs/api.md)
*   [Authentication API](docs/authAPI.md)
*   [User Management](docs/userAPI.md)
*   [Team Operations](docs/teamAPI.md)
*   [Game Logic](docs/gameAPI.md)
*   [Analytics Data](docs/analyticAPI.md)

Here is a summary of the key endpoints. **All endpoints except registration and login require a valid JWT token** in the `Authorization` header.

**Base URL:** `http://127.0.0.1:8000/api/`

### Authentication Endpoints
| Method | Endpoint | Description |
| :----- | :------- | :---------- |
| `POST` | `/auth/register/` | Register a new user (coach/player). |
| `POST` | `/auth/login/` | Login with email and password. Returns JWT tokens. |

### User Profile Endpoints
| Method | Endpoint | Description |
| :----- | :------- | :---------- |
| `GET` | `/auth/me/` | Retrieve the profile of the currently authenticated user. |
| `PUT`/`PATCH` | `/auth/me/` | Update the profile of the currently authenticated user. |

### Team Management Endpoints
| Method | Endpoint | Description | Access |
| :----- | :------- | :---------- | :----- |
| `GET` | `/teams/` | List all teams the authenticated user is a member of. | Member |
| `POST` | `/teams/` | Create a new team. The creator becomes the `COACH`. | Any User |
| `GET` | `/teams/{id}/` | Retrieve detailed information about a specific team. | Member |
| `PUT` | `/teams/{id}/` | Update team information (name, description). | Coach Only |
| `DELETE` | `/teams/{id}/` | Soft-delete a team. | Coach Only |
| `POST` | `/teams/join/` | Join a team using its 8-character join code. Role becomes `PLAYER`. | Any User |
| `GET` | `/teams/{team_id}/members/` | List all members of a specific team. | Member |
| `PUT` | `/teams/{team_id}/members/{member_id}/` | Update a player's `position` and `jersey_number`. | Coach Only |
| `DELETE` | `/teams/{team_id}/members/{member_id}/` | Remove a member from the team (soft-delete). | Coach Only |

### Game & Statistics Endpoints
| Method | Endpoint | Description | Access |
| :----- | :------- | :---------- | :----- |
| `GET` | `/teams/{team_id}/games/` | List all games for a specific team. | Member |
| `POST` | `/teams/{team_id}/games/` | Create a new game record for the team. | Coach Only |
| `GET` | `/games/{id}/` | Retrieve detailed information about a specific game, including all player stats. | Member |
| `PUT` | `/games/{id}/` | Update game details (scores, date, etc.). | Coach Only |
| `DELETE` | `/games/{id}/` | Permanently delete a game. | Coach Only |
| `POST` | `/games/{game_id}/stats/add/` | Add statistics for a single player in a specific game. | Coach Only |
| `GET` | `/games/{game_id}/stats/` | List all player statistics for a specific game. | Member |

### Analytics Endpoints
| Method | Endpoint | Description | Access |
| :----- | :------- | :---------- | :----- |
| `GET` | `/analytics/players/{player_id}/?team_id={id}` | Get average stats (PPG, APG, RPG, etc.) for a player. | Member |
| `GET` | `/analytics/teams/{team_id}/leaderboard/` | Get a team leaderboard for points, assists, rebounds, etc. | Member |
| `GET` | `/analytics/teams/{team_id}/trends/` | Get team performance trends (win %, quarter analysis, best/worst game). | Member |
| `GET` | `/analytics/games/{game_id}/` | Get a detailed analytics breakdown for a specific game (team totals, top scorer). | Member |

---

## Testing

The project includes a suite of unit tests to ensure core functionality works as expected.

To run all tests:
```bash
python manage.py test
```

---

## Architecture Overview

The project follows a standard Django MTV (Model-Template-View) pattern adapted for a RESTful API using Django REST Framework (DRF).

**Models (models.py):** Define the database structure. Key models include CustomUser, Team, TeamMember, Game, and PlayerStat.

**Serializers (serializers.py):** Act as a bridge between complex Python model instances and JSON. They handle validation and data transformation for API requests and responses.

**Views (views.py):** Contain the business logic for each API endpoint. They use DRF's generic views (like ListCreateAPIView) for efficiency and consistency, with custom permissions to enforce role-based access (coach vs. player).

**URLs (urls.py):** Route incoming HTTP requests to the appropriate view.

**Permissions:** Custom permission logic ensures that only coaches can create games or edit team details, while players have read-only access.

This separation of concerns makes the codebase modular, testable, and maintainable.

---

## Project Structure

<details>
<summary><b>Click to view Project Structure</b></summary>

```text
Alx_CapstoneProject_CourtsideAnalytics/
├── courtside_analytics/          # Project configuration directory
│   ├── courtside_analytics/       # Inner project folder (settings, urls)
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   └── urls.py
│   ├── apps/                      # All Django apps
│   │   ├── users/
│   │   ├── teams/
│   │   ├── games/
│   │   └── analytics/
│   ├── templates/                 # Basic HTML templates (optional)
│   └── manage.py
├── docs/                           # Markdown API documentation
│   ├── authAPI.md
│   ├── userAPI.md
│   ├── teamAPI.md
│   ├── gameAPI.md
│   ├── analyticAPI.md
│   └── api.md                      # Main API overview
├── .env                            # Environment variables (ignored by git)
├── .env.example                    # Example environment variables
├── .gitignore
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

</details>

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Please take a moment to review my [Contributing Guidelines](CONTRIBUTING.md) before you get started. They contain important information about:

- How to report bugs and suggest features
- Coding standards (PEP 8, Django best practices)
- The pull request process
- Setting up your development environment

We also use [GitHub Issues](https://github.com/RobertJanam/Alx_CapstoneProject_CourtsideAnalytics/issues) to track tasks. Look for issues labeled `good first issue` if you're just getting started!

---

## Contact & Credits

**Project Maintainer:** RobertJanam

* **Project Link:** https://github.com/RobertJanam/Alx_CapstoneProject_CourtsideAnalytics

**Acknowledgments:**

This project was built as part of the ALX Backend Engineering Capstone.

* **Thanks to the ALX community and mentors for their guidance:** https://www.alxafrica.com/

Inspired by the need for better sports analytics tools in Kenyan grassroots basketball.

<p align="center">Made with appreciation for Kenyan Basketball</p>