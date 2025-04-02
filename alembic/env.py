# /alembic/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env or .env.production based on RENDER flag
RENDER = os.getenv("RENDER", "").lower() == "true"
env_file = ".env.production" if RENDER else ".env"
env_path = Path(__file__).resolve().parent.parent / "backend" / env_file
load_dotenv(dotenv_path=env_path)

# This is the Alembic Config object, which provides access to values within alembic.ini.
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the sqlalchemy URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL not set in environment!")

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Import your metadata
from backend.data.database.models import Base  # adjust if needed

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
