from __future__ import with_statement
from logging.config import fileConfig
import sys
import os

# File-based debug logging
def log_debug(msg):
    try:
        with open('/media/eoex/DOJO/CONSULTING/PROJECTS/TEST/ryze/alembic_env_debug.log', 'a') as f:
            f.write(str(msg) + '\n')
    except Exception as e:
        pass

log_debug('[alembic.env.py] --- env.py execution started ---')
from sqlalchemy import engine_from_config, pool
from alembic import context
from os import path

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Ensure project root is on sys.path so 'app_server' can be imported
project_root = path.abspath(path.join(path.dirname(__file__), '..'))
log_debug(f"[alembic.env.py] sys.path before: {sys.path}")
if project_root not in sys.path:
    sys.path.insert(0, project_root)
log_debug(f"[alembic.env.py] sys.path after: {sys.path}")

# Override sqlalchemy.url from env var DATABASE_URL
db_url = os.environ.get('DATABASE_URL')
if db_url:
    # Normalize common provider URLs to SQLAlchemy dialects
    if db_url.startswith('mysql://'):
        db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
    # Render often provides "postgres://" which SQLAlchemy doesn't accept; use postgresql+psycopg2
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
    config.set_main_option('sqlalchemy.url', db_url)

# add your model's MetaData object here for 'autogenerate' support
# from yourapp import yourmodel
# target_metadata = yourmodel.Base.metadata
try:
    from app_server import db  # noqa: E402
    log_debug(f"[alembic.env.py] db: {db}")
    log_debug(f"[alembic.env.py] db.metadata: {getattr(db, 'metadata', None)}")
    target_metadata = db.metadata
except Exception as e:
    log_debug(f"[alembic.env.py] ERROR importing db from app_server: {e}")
    target_metadata = None

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
