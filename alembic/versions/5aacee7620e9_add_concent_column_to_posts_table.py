"""add concent column to posts table

Revision ID: 5aacee7620e9
Revises: 43a94318b0c3
Create Date: 2023-05-02 10:55:43.709005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5aacee7620e9'
down_revision = '43a94318b0c3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
