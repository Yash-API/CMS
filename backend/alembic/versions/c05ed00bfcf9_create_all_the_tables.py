"""Create all the tables"""

revision = 'c05ed00bfcf9'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('role', sa.String, nullable=False),
        sa.Column('salary', sa.Float, nullable=False),
        sa.Column('joining_date', sa.Date, nullable=False),
        sa.Column('dob', sa.Date, nullable=True),
    )
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False, index=True),
        sa.Column('budget', sa.Float, nullable=False),
        sa.Column('project_description', sa.String, nullable=True),
        sa.Column('project_start_date', sa.Date, nullable=False),
        sa.Column('project_end_date', sa.Date, nullable=True),
        sa.Column('total_payment_received', sa.Integer, nullable=True),
        sa.Column('payment_received_account', sa.Integer, nullable=True),
        sa.Column('pending_payment', sa.Integer, nullable=True),
    )
    op.create_table(
        'client_payments',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('client_id', sa.Integer, sa.ForeignKey('clients.id'), nullable=False),
        sa.Column('payment_received_date', sa.Date, nullable=False),
        sa.Column('payment_received_amount', sa.Integer, nullable=False),
    )
    op.create_table(
        'predefined_queries',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('question', sa.String, nullable=False, index=True),
        sa.Column('sql_query', sa.String, nullable=False),
    )


def downgrade():
    op.drop_table('predefined_queries')
    op.drop_table('client_payments')
    op.drop_table('clients')
    op.drop_table('employees')
