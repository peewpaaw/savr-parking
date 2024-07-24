"""accident-user relationship

Revision ID: 71e3925a6987
Revises: ad611f0aeef5
Create Date: 2024-07-24 14:09:18.119544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71e3925a6987'
down_revision = 'ad611f0aeef5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accident', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('accident_created_by_fkey', 'accident', type_='foreignkey')
    op.create_foreign_key(None, 'accident', 'user', ['user_id'], ['id'])
    op.drop_column('accident', 'created_by')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accident', sa.Column('created_by', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.create_foreign_key('accident_created_by_fkey', 'accident', 'user', ['created_by'], ['id'])
    op.drop_column('accident', 'user_id')
    # ### end Alembic commands ###
