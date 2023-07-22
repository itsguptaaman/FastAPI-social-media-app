"""Add last few columns to the posts

Revision ID: ac174bd1a501
Revises: bf67a222ff89
Create Date: 2023-07-22 18:21:02.030969

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ac174bd1a501'
down_revision = 'bf67a222ff89'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=True, server_defoult='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                                     server_defoult=sa.text('NOW()')),)


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
