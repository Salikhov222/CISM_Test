"""delete_TaskStatuses

Revision ID: fc03e2b41a56
Revises: 0142f4287bb8
Create Date: 2024-12-14 15:45:34.701680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fc03e2b41a56'
down_revision: Union[str, None] = '0142f4287bb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks_statuses')
    op.add_column('tasks', sa.Column('status', sa.String(), nullable=False))
    op.create_check_constraint(
        "valid_status_check",
        "tasks",
        "status IN ('new', 'in_progress', 'completed', 'error')"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'status')
    op.create_table('tasks_statuses',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('task_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('changed_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.CheckConstraint("status::text = ANY (ARRAY['new'::character varying, 'in_progress'::character varying, 'completed'::character varying, 'error'::character varying]::text[])", name='valid_status_check'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='tasks_statuses_task_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='tasks_statuses_pkey')
    )
    # ### end Alembic commands ###
