"""auto votes

Revision ID: 378485bacfe0
Revises: ac174bd1a501
Create Date: 2023-07-22 18:31:26.180572

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '378485bacfe0'
down_revision = 'ac174bd1a501'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    )
    op.drop_table('products')
    op.alter_column('posts', 'published',
                    existing_type=mysql.TINYINT(display_width=1),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'published',
                    existing_type=mysql.TINYINT(display_width=1),
                    nullable=True)
    op.create_table('products',
                    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
                    sa.Column('price', mysql.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('sale', mysql.TINYINT(display_width=1), server_default=sa.text("'0'"),
                              autoincrement=False, nullable=True),
                    sa.Column('inventory', mysql.INTEGER(), server_default=sa.text("'0'"), autoincrement=False,
                              nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_collate='utf8mb4_0900_ai_ci',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB'
                    )
    op.drop_table('votes')
    # ### end Alembic commands ###
