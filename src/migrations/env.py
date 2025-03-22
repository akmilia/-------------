from logging.config import dictConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from apps.users.models import Base  # noqa: F403 
from core.log import config as log_config
from database import db_manager 
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Field
 

target_metadata = Base.metadata

class Schedule(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    dateandtime: datetime
    weakday: str = Field(max_length=45) 

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    return config.get_main_option("sqlalchemy.url")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the script
    directly to the console.  
    """
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(get_url())

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
# dictConfig(log_config)


# config = context.config
# url = db_manager.sync_url
# target_metadata = SQLModel.metadata


# def run_migrations_offline() -> None:
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={'paramstyle': 'named'},
#     )

#     with context.begin_transaction():
#         context.run_migrations()


# def run_migrations_online() -> None:
#     cfg = config.get_section(config.config_ini_section, {})
#     cfg['sqlalchemy.url'] = url
#     connectable = engine_from_config(
#         cfg,
#         prefix='sqlalchemy.',
#         poolclass=pool.NullPool,
#     )

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection, target_metadata=target_metadata, render_as_batch=True
#         )

#         with context.begin_transaction():
#             context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()
