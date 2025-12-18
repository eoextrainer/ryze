# Project Planning and Overview

## Project Goals
- Build a basketball platform for clubs and players with subscription tiers, dashboards, and credential management.
- Support for club and player logins, data seeding, and robust error workflows.

## Key Features
- Flask backend with SQLAlchemy ORM
- Alembic migrations for database schema
- Data seeding for clubs, players, stats, and performances
- Render.com hosting configuration for web server and database
- Automated credential verification and error handling

---

# Configuration and Installation

## Prerequisites
- Python 3.12+
- pip, venv
- Git
- Render.com account (for deployment)

## Local Setup
1. Clone the repository:
   ```sh
   git clone git@github.com:eoextrainer/ryze.git
   cd ryze
   ```
2. Create and activate a virtual environment:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   pip install alembic
   ```
4. Initialize the database:
   ```sh
   alembic upgrade head
   ```
5. Seed the database:
   ```sh
   python scripts/seed_db.py
   ```
6. Verify setup:
   ```sh
   python verify_database.py
   ```

---

# Error Corrections and Workflow

- If the database is corrupted, delete `instance/dunes_basketball.db`, re-run Alembic migrations, and reseed.
- Ensure `alembic.ini` uses the correct SQLite URL for local development.
- All credential and login workflows are verified by running `verify_database.py`.

---

# Dependency Management

- All Python dependencies are listed in `requirements.txt`.
- Alembic is required for migrations and should be installed manually if not present.

---

# Render Hosting Configuration

## Web Server
- Use `render.yaml` for Render.com service definition.
- `app.py` is the main entry point for the Flask server.

## Database
- Use Render PostgreSQL or MySQL for production.
- For local development, SQLite is used (`instance/dunes_basketball.db`).
- Set `DATABASE_URL` environment variable for production deployments.

---

# Git Workflows

- Save, stash, stage, commit, and push changes using standard git commands:
  ```sh
  git add .
  git commit -m "Update project structure and documentation"
  git push origin main
  ```
- Always include all hidden files (e.g., `.env`, `.venv`, `.gitignore`) in backups/archives.

---

# Archiving

- To create a zip archive:
  ```sh
  zip -r ryze.zip .
  ```
- To create a tar.gz archive:
  ```sh
  tar czvf ryze.tar.gz .
  ```

---

# Folder Structure (Recommended)

- `alembic/` - Database migrations
- `instance/` - SQLite database and instance files
- `scripts/` - Data seeding and utility scripts
- `static/` - Static assets (JS, CSS, images)
- `templates/` - HTML templates
- `tests/` - Test scripts
- `doc/` - Documentation and credentials
- `res/` - Brand and design resources
- `cms-v2/` - CMS runtime files
- Root: Main app files, configs, Dockerfile, Makefile, etc.

---

# Notes
- Keep all configuration and documentation up to date for maintainability and onboarding.
- For any issues, review the error correction and workflow section above.
