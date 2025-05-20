"""Create client Table"""

revision = 'd54abce03cc9'
down_revision = '54adebb564b8'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('budget', sa.Float(), nullable=True),
        sa.Column('project_description', sa.String(), nullable=True),
        sa.Column('project_start_date', sa.Date(), nullable=True),
        sa.Column('project_end_date', sa.Date(), nullable=True),
        sa.Column('total_payment_received', sa.Integer(), nullable=True),
        sa.Column('payment_received_account', sa.Integer(), nullable=True),
        sa.Column('pending_payment', sa.Integer(), nullable=True),
    )
    op.create_index(op.f('ix_clients_id'), 'clients', ['id'], unique=False)
    op.create_index(op.f('ix_clients_name'), 'clients', ['name'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_clients_name'), table_name='clients')
    op.drop_index(op.f('ix_clients_id'), table_name='clients')
    op.drop_table('clients')

