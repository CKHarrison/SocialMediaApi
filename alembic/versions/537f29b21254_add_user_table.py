"""add user table

Revision ID: 537f29b21254
Revises: 5aacee7620e9
Create Date: 2023-05-02 11:02:41.482410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '537f29b21254'
down_revision = '5aacee7620e9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table('users')
