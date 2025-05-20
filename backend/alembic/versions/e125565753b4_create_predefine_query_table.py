"""Create Predefine_query Table"""

revision = 'e125565753b4'
down_revision = '79854943a722'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'predefined_queries',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('question', sa.String(), nullable=True),
        sa.Column('sql_query', sa.String(), nullable=False),
    )
    op.create_index(op.f('ix_predefined_queries_id'), 'predefined_queries', ['id'], unique=False)
    op.create_index(op.f('ix_predefined_queries_question'), 'predefined_queries', ['question'], unique=False)

def downgrade():
    try:
        op.drop_index(op.f('ix_predefined_queries_question'), table_name='predefined_queries')
    except:
        pass
    try:
        op.drop_index(op.f('ix_predefined_queries_id'), table_name='predefined_queries')
    except:
        pass
    try:
        op.drop_table('predefined_queries')
    except:
        pass

