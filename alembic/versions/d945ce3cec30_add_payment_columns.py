"""add payment columns

Revision ID: d945ce3cec30
Revises: 60400129636a
Create Date: 2026-05-09 10:23:50.730656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd945ce3cec30'
down_revision: Union[str, Sequence[str], None] = '60400129636a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add the new Razorpay columns and status
    op.add_column('payments', sa.Column('razorpay_order_id', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('razorpay_payment_id', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('razorpay_signature', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('status', sa.String(), nullable=True, server_default='PENDING'))
    op.add_column('payments', sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()))
    op.create_index(op.f('ix_payments_razorpay_order_id'), 'payments', ['razorpay_order_id'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_payments_razorpay_order_id'), table_name='payments')
    op.drop_column('payments', 'created_at')
    op.drop_column('payments', 'status')
    op.drop_column('payments', 'razorpay_signature')
    op.drop_column('payments', 'razorpay_payment_id')
    op.drop_column('payments', 'razorpay_order_id')
    # ### end Alembic commands ###
