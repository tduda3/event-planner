"""Initial schema

Revision ID: 970db1fb4a00
Revises: 
Create Date: 2025-07-23 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = '970db1fb4a00'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=80), nullable=False, unique=True),
        sa.Column('email', sa.String(length=120), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
    )
    op.create_table(
        'events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('datetime', sa.DateTime(), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
    )
    op.create_table(
        'registrations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('event_id', sa.Integer(), sa.ForeignKey('events.id', ondelete='CASCADE'), nullable=False),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('registrations')
    op.drop_table('events')
    op.drop_table('users')
