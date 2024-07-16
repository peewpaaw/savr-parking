"""init

Revision ID: e795fc8b196f
Revises: 
Create Date: 2024-07-15 17:44:06.219973

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e795fc8b196f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accident',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('note', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accident')
    # ### end Alembic commands ###