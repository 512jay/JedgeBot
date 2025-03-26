# /alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from dotenv import load_dotenv

# ---------------------------------------------------------------------
# Load environment variables from .env.auth
# ---------------------------------------------------------------------
env_path = os.path.join(
    os.path.dirname(__file__), "../backend/data/database/auth/.env.auth"
)
load_dotenv(dotenv_path=env_path)

# ---------------------------------------------------------------------
# Import your models' Base class
# ---------------------------------------------------------------------
from backend.data.database.models import Base


# Alembic Config
config = context.config
if config.config_file_name is not None:
    fileConfig(fname=str(config.config_file_name))  # type: ignore[arg-type]

# Inject DB URL into Alembic config
DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Assign metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
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
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
