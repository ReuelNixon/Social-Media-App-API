"""Creating post table

Revision ID: e199a9247e04
Revises: 
Create Date: 2023-03-22 19:16:30.851639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e199a9247e04'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False), 
                            sa.Column('title', sa.String(), nullable=False), 
                            sa.Column('content', sa.String(), nullable=False),
                            sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('posts')
