"""Initialize

Revision ID: 51eaf196b3e8
Revises: 
Create Date: 2023-07-29 22:34:18.891709

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '51eaf196b3e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'project',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_project'))
    )
    op.create_table(
        'wage',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('currency', sqlmodel.sql.sqltypes.AutoString(length=3), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['project.id'], name=op.f('fk_wage_project_id_project')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_wage'))
    )
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.Column('start', sa.DateTime(), nullable=False),
        sa.Column('end', sa.DateTime(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['project.id'], name=op.f('fk_task_project_id_project')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_task'))
    )


def downgrade():
    op.drop_table('task')
    op.drop_table('wage')
    op.drop_table('project')
