"""Create client_payment Table"""

revision = '79854943a722'
down_revision = 'd54abce03cc9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'client_payments',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('client_id', sa.Integer(), sa.ForeignKey('clients.id'), nullable=True),
        sa.Column('payment_received_date', sa.Date(), nullable=True),
        sa.Column('payment_received_amount', sa.Integer(), nullable=True),
    )
    op.create_index(op.f('ix_client_payments_id'), 'client_payments', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_client_payments_id'), table_name='client_payments')
    op.drop_table('client_payments')

