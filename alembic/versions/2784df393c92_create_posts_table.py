"""create posts table

Revision ID: 2784df393c92
Revises: 
Create Date: 2022-06-27 17:25:35.281234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2784df393c92'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(),  nullable=False, primary_key=True),
                             sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass

