# Contributing to Basketball Courtside Analytics & Tracker

First off, thank you for considering contributing to this project! It's people like you that make this tool better for Kenyan basketball.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [robertbjanam@gmail.com].

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [existing issues](https://github.com/RobertJanam/Alx_CapstoneProject_CourtsideAnalytics/issues) to see if the problem has already been reported. If it hasn't, [open a new issue](https://github.com/RobertJanam/Alx_CapstoneProject_CourtsideAnalytics/issues/new) and include:

- **A clear and descriptive title**
- **Steps to reproduce** the behavior
- **Expected behavior** vs **actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, Django version)

### Suggesting Enhancements

Enhancement suggestions are tracked as [GitHub issues](https://github.com/RobertJanam/Alx_CapstoneProject_CourtsideAnalytics/issues). When creating an enhancement suggestion, please include:

- **A clear and descriptive title**
- **A detailed description** of the proposed functionality
- **Explain why this would be useful** to most users
- **Code examples** or **mockups** if relevant

### Your First Code Contribution

Unsure where to begin? You can start by looking through `good first issue` and `help wanted` issues:

- [Good First Issues](https://github.com/RobertJanam/Alx_CapstoneProject_CourtsideAnalytics/labels/good%20first%20issue) - tasks that should only require a few lines of code and minimal context.
- [Help Wanted Issues](https://github.com/RobertJanam/Alx_CapstoneProject_CourtsideAnalytics/labels/help%20wanted) - tasks that are more involved but still approachable.

---

## Development Setup

Follow the [installation instructions](README.md#-getting-started) in the README to get your local environment up and running. Here's a quick recap:

1. Fork and clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set up your `.env` file (copy from `.env.example`)
5. Create the database and run migrations: `python manage.py migrate`
6. Run the development server: `python manage.py runserver`

Make sure all tests pass before you start making changes:
```bash
python manage.py test
```

---

## Coding Standards

We strive to maintain a clean and consistent codebase. Please adhere to the following standards:

### Python & Django
Follow PEP 8 style guide.

Use tabs for indentation.

Use meaningful variable and function names.

### Django-Specific
App names should be plural (e.g., teams, games).

Model classes should be singular (e.g., Team, Game).

Use snake_case for URLs and function names.

Use CamelCase for class names.

### Git Commit Messages
You can use present or past tense("Add feature" or "Added feature").

Use the imperative or indicative mood("Move cursor to..." or "Moves cursor to...").

Limit the first line to 50 characters.

Reference issues and pull requests liberally after the first line.

*Example:*

```text
feat: Added player averages endpoint

- Implemented PlayerAnalyticsView
- Added get_player_averages utility function
- Updated analytics URLs
```

---

## Pull Request Process
Fork the repository and create your branch from main.

```bash
git checkout -b feature/your-feature-name
```

Make your changes, following the coding standards above.

Write or update tests as needed (Using AI is allowed). Ensure all tests pass:

```bash
python manage.py test
```

or (for individual apps)

```bash
    python manage.py test apps.users
    python manage.py test apps.games
    python manage.py test apps.teams
    python manage.py test apps.analytics
```

### Update documentation
(README.md, API docs, etc.)
if your changes require it (Using AI for reference is allowed. If you must copy paste the AI's work, ensure it follows the correct structure. Update table of contents if necessary).

Commit your changes with a clear commit message.

Push to your fork and submit a pull request.

**Describe your pull request:**

- What does this PR do?

- How can it be tested?

- Screenshots (if applicable)

- Related issues

### Review Process
Maintainers will review your PR as soon as possible.

They may request changes or ask questions.

Once approved, a maintainer will merge your PR.

Thank you for contributing!