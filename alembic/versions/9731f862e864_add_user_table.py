"""add user table

Revision ID: 9731f862e864
Revises: edec4749dee9
Create Date: 2023-07-22 13:59:18.362846

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9731f862e864'
down_revision = 'edec4749dee9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(255), nullable=False),
                    sa.Column('password', sa.String(255), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table("users")

