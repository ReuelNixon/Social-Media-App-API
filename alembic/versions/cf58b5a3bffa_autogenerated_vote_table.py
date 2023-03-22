"""Autogenerated vote table

Revision ID: cf58b5a3bffa
Revises: 0a26d72fdc7f
Create Date: 2023-03-22 19:54:25.525886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf58b5a3bffa'
down_revision = '0a26d72fdc7f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('pid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pid'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['uid'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid', 'pid')
    )
    op.add_column('posts', sa.Column('uid', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.drop_constraint('post_users_fk', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['uid'], ['id'], ondelete='CASCADE')
    op.drop_column('posts', 'owner_id')
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.add_column('posts', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('post_users_fk', 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_column('posts', 'uid')
    op.drop_table('votes')
    # ### end Alembic commands ###