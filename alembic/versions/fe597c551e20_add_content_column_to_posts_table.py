"""add content column to posts table

Revision ID: fe597c551e20
Revises: 2784df393c92
Create Date: 2022-06-27 17:55:33.461850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe597c551e20'
down_revision = '2784df393c92'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

