"""
empty message

Revision ID: e6a840f2510f
Revises: f7ff4d5b7b48
Create Date: 2025-03-05 13:40:13.637493

"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e6a840f2510f'
down_revision: str | None = 'f7ff4d5b7b48'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


if not sqlmodel.sql:
    raise Exception('Something went wrong')


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'schedule',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dateandtime', sa.DateTime(), nullable=False),
        sa.Column('student_class', sqlmodel.sql.sqltypes.AutoString(length=45), nullable=False),
        sa.Column('teacher_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['teacher_id'],
            ['user.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
    )
    op.create_table(
        'schedule_cabinet',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('schedule_id', sa.Integer(), nullable=False),
        sa.Column('cabinet_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['cabinet_id'],
            ['cabinet.id'],
        ),
        sa.ForeignKeyConstraint(
            ['schedule_id'],
            ['schedule.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
    )
    op.create_table(
        'schedule_subject',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('schedule_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['schedule_id'],
            ['schedule.id'],
        ),
        sa.ForeignKeyConstraint(
            ['subject_id'],
            ['subject.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schedule_subject')
    op.drop_table('schedule_cabinet')
    op.drop_table('schedule')
    # ### end Alembic commands ###
