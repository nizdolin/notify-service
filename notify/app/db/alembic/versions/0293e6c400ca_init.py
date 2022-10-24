"""init

Revision ID: 0293e6c400ca
Revises: 
Create Date: 2021-02-11 11:59:00.714012

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0293e6c400ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('user_id', postgresql.UUID(), nullable=True),
    sa.Column('storage_id', postgresql.UUID(), nullable=True),
    sa.Column('storage_address', sa.String(length=100), nullable=True),
    sa.Column('storage_type', sa.Enum('cloud', 'self_storage', name='storagetype'), nullable=True),
    sa.Column('total', sa.Float(), nullable=True),
    sa.Column('date_from', sa.DateTime(), nullable=True),
    sa.Column('period_type', sa.Enum('week', 'month', name='periodtype'), nullable=True),
    sa.Column('discount_id', postgresql.UUID(), nullable=True),
    sa.Column('periods_number', sa.Integer(), nullable=True),
    sa.Column('invoice_id', sa.String(), nullable=True),
    sa.Column('unit_id', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_id'), 'order', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_id'), table_name='order')
    op.drop_table('order')
    # ### end Alembic commands ###