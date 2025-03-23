[alembic]
script_location = migrations
file_template = %%(year)d.%%(month).2d.%%(day).2d_%%(hour).2d-%%(minute).2d-%%(second).2d_%%(rev)s
output_encoding = utf-8
prepend_sys_path = ./src
version_path_separator = os
[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S

sqlalchemy.url = postgresql+psycopg2://postgres:2006@localhost:5432/diplom_school

; sqlalchemy.url = postgresql://postgres:2006@localhost:5432/diplom_school
; DATABASE_URL = "postgresql://postgres:2006@localhost:5432/diplom_school" 


---------------------------------------------------------------------------- 


from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

import sys
import os

# Добавьте путь к вашему проекту в sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import Base
target_metadata = Base.metadata


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline():
    # Код для оффлайн-миграций
    pass

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
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
