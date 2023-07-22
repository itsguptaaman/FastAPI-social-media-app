"""add content column to post table

Revision ID: edec4749dee9
Revises: aec7ced4b4d1
Create Date: 2023-07-22 13:43:54.011687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edec4749dee9'
down_revision = 'aec7ced4b4d1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(255), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
