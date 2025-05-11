from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys

# Add app directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from database import Base  # Import Base from app.database
from database import DATABASE_URL  # Import DATABASE_URL from app.database

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override sqlalchemy.url with DATABASE_URL from environment or app.database
config.set_main_option('sqlalchemy.url', DATABASE_URL)

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
