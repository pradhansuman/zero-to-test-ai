"""Add Phase 4 analytics tables.

Revision ID: 004_phase4_analytics
Revises: 003_phase3_tables
Create Date: 2026-07-03 13:50:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '004_phase4_analytics'
down_revision = '003_phase3_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create Phase 4 analytics tables."""
    # Create metrics table
    op.create_table(
        'metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('metric_type', sa.String(50), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_metrics_project_id', 'project_id'),
        sa.Index('ix_metrics_timestamp', 'timestamp'),
    )

    # Create dashboard_configs table
    op.create_table(
        'dashboard_configs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('layout', sa.JSON(), nullable=True),
        sa.Column('widgets', sa.JSON(), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=False),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_dashboard_configs_user_id', 'user_id'),
        sa.Index('ix_dashboard_configs_project_id', 'project_id'),
    )

    # Create custom_widgets table
    op.create_table(
        'custom_widgets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dashboard_id', sa.Integer(), nullable=False),
        sa.Column('widget_type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('metric_keys', sa.JSON(), nullable=True),
        sa.Column('time_range', sa.String(20), nullable=False),
        sa.Column('aggregation', sa.String(20), nullable=False),
        sa.Column('config', sa.JSON(), nullable=True),
        sa.Column('position', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['dashboard_id'], ['dashboard_configs.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_custom_widgets_dashboard_id', 'dashboard_id'),
    )


def downgrade() -> None:
    """Drop Phase 4 analytics tables."""
    op.drop_table('custom_widgets')
    op.drop_table('dashboard_configs')
    op.drop_table('metrics')
