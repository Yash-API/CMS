"""Create employee Table"""

revision = '54adebb564b8'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('salary', sa.Float(), nullable=True),
        sa.Column('joining_date', sa.Date(), nullable=True),
        sa.Column('dob', sa.Date(), nullable=True),
    )
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_employees_id'), table_name='employees')
    op.drop_table('employees')