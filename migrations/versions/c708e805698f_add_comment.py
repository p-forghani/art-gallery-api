"""Add comment

Revision ID: c708e805698f
Revises: 1e412623b61f
Create Date: 2025-05-27 23:37:49.237564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c708e805698f'
down_revision = '1e412623b61f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('upvotes')
    op.drop_table('comments')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('artwork_id', sa.INTEGER(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['artwork_id'], ['artwork.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('upvotes',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('artwork_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['artwork_id'], ['artwork.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###
