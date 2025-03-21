"""
empty message

Revision ID: 40b043a6cb94
Revises: 5a6f7b854006
Create Date: 2025-03-06 09:39:58.038361

"""
from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '40b043a6cb94'
down_revision: str | None = '5a6f7b854006'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


if not sqlmodel.sql:
    raise Exception('Something went wrong')


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schedule_user')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('student_class')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_class', sa.VARCHAR(length=45), nullable=True))

    op.create_table('schedule_user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('schedule_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###
