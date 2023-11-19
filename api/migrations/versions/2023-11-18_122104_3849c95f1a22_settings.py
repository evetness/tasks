"""Settings

Revision ID: 3849c95f1a22
Revises: 51eaf196b3e8
Create Date: 2023-11-18 12:21:04.217104

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = '3849c95f1a22'
down_revision = '51eaf196b3e8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'setting',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('language', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_setting'))
    )


def downgrade():
    op.drop_table('setting')
