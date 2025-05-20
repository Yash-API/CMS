"""recreate_predefined_queries_table"""

revision = '9a43718a0940'
down_revision = 'e125565753b4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Drop the table if it exists (shouldn't exist, but just in case)
    op.drop_table('predefined_queries', if_exists=True)
    
    # Create the table
    op.create_table(
        'predefined_queries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question', sa.String(), nullable=True),
        sa.Column('sql_query', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_predefined_queries_id'), 'predefined_queries', ['id'], unique=False)
    op.create_index(op.f('ix_predefined_queries_question'), 'predefined_queries', ['question'], unique=False)


def downgrade():
    # Drop indexes first
    op.drop_index(op.f('ix_predefined_queries_question'), table_name='predefined_queries')
    op.drop_index(op.f('ix_predefined_queries_id'), table_name='predefined_queries')
    
    # Drop the table
    op.drop_table('predefined_queries')
