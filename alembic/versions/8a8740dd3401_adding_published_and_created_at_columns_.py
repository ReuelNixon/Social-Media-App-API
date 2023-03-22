"""Adding published and created_at columns to post table

Revision ID: 8a8740dd3401
Revises: ff3d05b386bf
Create Date: 2023-03-22 19:35:03.802553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a8740dd3401'
down_revision = 'ff3d05b386bf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'is_published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)


def downgrade() -> None:
    op.drop_column('posts', 'is_published')
    op.drop_column('posts', 'created_at')
