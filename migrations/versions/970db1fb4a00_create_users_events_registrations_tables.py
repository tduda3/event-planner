"""Create users, events, registrations tables

Revision ID: 970db1fb4a00
Revises: a3716dd2eedf
Create Date: 2025-07-22 12:49:34.979566

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '970db1fb4a00'
down_revision = 'a3716dd2eedf'
branch_labels = None
dependencies = None


def upgrade():
    # Rename legacy tables rather than drop to preserve FKs and data
    op.rename_table('user', 'users')
    op.rename_table('event', 'events')
    op.rename_table('registration', 'registrations')

    # Create 'users' table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )

    # Create 'events' table
    op.create_table(
        'events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('datetime', sa.DateTime(), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create 'registrations' table
    op.create_table(
        'registrations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['event_id'], ['events.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop new tables
    op.drop_table('registrations')
    op.drop_table('events')
    op.drop_table('users')

    # Rename tables back to legacy names
    op.rename_table('registrations', 'registration')
    op.rename_table('events', 'event')
    op.rename_table('users', 'user')