# Render Environment Variable Example

# In your Render web service settings, add the following environment variable:

Key: DATABASE_URL
Value: mysql://<USER>:<PASSWORD>@<HOST>:<PORT>/dunes_basketball

# Replace <USER>, <PASSWORD>, <HOST>, and <PORT> with your Render MySQL database credentials.

---

# Alembic Migration Command Example (run in Render shell or locally with DATABASE_URL set):

# If running in Render shell:
alembic upgrade head

# If running locally (Linux/macOS):
export DATABASE_URL="mysql://<USER>:<PASSWORD>@<HOST>:<PORT>/dunes_basketball"
alembic upgrade head

# If running locally (Windows CMD):
set DATABASE_URL=mysql://<USER>:<PASSWORD>@<HOST>:<PORT>/dunes_basketball
alembic upgrade head

# This will apply all migrations to your MySQL database.
