from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from currency.db.base import Model
from currency.settings.settings import settings


config = context.config


def get_url() -> str:
    user = settings.DB_USER
    password = settings.DB_PASSWORD
    server = settings.DB_HOST
    port = settings.DB_PORT
    db = settings.DB_DATABASE

    return f"postgresql://{user}:{password}@{server}:{port}/{db}"


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Model.metadata


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url()
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
