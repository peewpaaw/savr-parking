"""subject with statuses

Revision ID: bfc8c9223afa
Revises: 6b88e0a9b418
Create Date: 2024-07-25 11:20:59.940373

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bfc8c9223afa'
down_revision = '6b88e0a9b418'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subject',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('type', postgresql.ENUM('vehicle', 'mobile', name='subjecttype'), nullable=False),
    sa.Column('bts_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('subject_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_uuid', sa.UUID(), nullable=True),
    sa.Column('datetime_entry', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.Column('datetime_unix', sa.BIGINT(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('speed', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['subject_uuid'], ['subject.uuid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subject_status')
    op.drop_table('subject')
    # ### end Alembic commands ###
