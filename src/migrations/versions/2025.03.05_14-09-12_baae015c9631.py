"""
empty message

Revision ID: baae015c9631
Revises: e6a840f2510f
Create Date: 2025-03-05 14:09:12.730150

"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'baae015c9631'
down_revision: str | None = 'e6a840f2510f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


if not sqlmodel.sql:
    raise Exception('Something went wrong')


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    users_table = sa.table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('surname', sqlmodel.sql.sqltypes.AutoString(length=45), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=45), nullable=False),
        sa.Column('paternity', sqlmodel.sql.sqltypes.AutoString(length=45), nullable=True),
        sa.Column('gender', sqlmodel.sql.sqltypes.AutoString(length=45), nullable=True),
        sa.Column('birthdate', sa.DateTime(), nullable=True),
        sa.Column('login', sqlmodel.sql.sqltypes.AutoString(length=25), nullable=False),
        sa.Column('password', sqlmodel.sql.sqltypes.AutoString(length=25), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
    )

    op.bulk_insert(
        users_table,
        [
            {
                'id': 2,
                'surname': 'Фамилия',
                'name': 'Имя',
                'paternity': 'Отчество',
                'gender': 'teacher',
                'birthdate': None,
                'login': 'teacher',
                'password': 'teacher',
                'role_id': 2,
            }
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
