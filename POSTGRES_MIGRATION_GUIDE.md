# Migrating to PostgreSQL for Render

Follow these steps to migrate your Flask backend from MySQL/SQLite to PostgreSQL for Render deployment:

## 1. Provision a PostgreSQL Database on Render
- In your Render dashboard, create a new PostgreSQL database service.
- Note the connection string (e.g., `postgres://USER:PASSWORD@HOST:PORT/DBNAME`).

## 2. Update Your Environment Variable
- In your Render web service, go to the "Environment" tab.
- Add or update the following variable:
  - Key: `DATABASE_URL`
  - Value: (Paste your PostgreSQL connection string from above)

## 3. Ensure psycopg2-binary is Installed
- Your `requirements.txt` already includes `psycopg2-binary`. No changes needed.

## 4. Update Local Development (Optional)
- For local testing, you can use SQLite or a local PostgreSQL instance.
- To use PostgreSQL locally, set `DATABASE_URL` in your shell:
  - Linux/macOS: `export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME`
  - Windows CMD: `set DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME`

## 5. Run Alembic Migrations
- In your Render shell or locally (with `DATABASE_URL` set), run:
  ```
  alembic upgrade head
  ```
- This will create all tables in your PostgreSQL database.

## 6. Verify the Connection
- Deploy your app on Render.
- Visit `/verify_db` on your deployed app to confirm the database is connected and tables are accessible.

## 7. (Optional) Data Migration
- If you have existing data in SQLite/MySQL, export and import it into PostgreSQL using tools like `pgloader` or manual scripts.

---

Your codebase is already compatible with PostgreSQL via SQLAlchemy. No code changes are required unless you use raw SQL queries with MySQL-specific syntax.
