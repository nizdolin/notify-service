"""init

Revision ID: 21b2a4a176f3
Revises: 
Create Date: 2022-10-25 12:09:19.206726

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '21b2a4a176f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=False)
    op.create_table('notification',
    sa.Column('type', sa.Enum('base', 'quest_request', name='notificationtype'), nullable=True),
    sa.Column('text', sa.TEXT(), nullable=True),
    sa.Column('extra', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('sender_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('viewed', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notification')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###