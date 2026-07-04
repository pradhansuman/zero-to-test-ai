"""Add performance indexes for Phase 3 tasks.

Revision ID: 008
Revises: 007
Create Date: 2026-07-03
"""
from alembic import op
import sqlalchemy as sa

revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('CREATE INDEX idx_execution_status ON executions(status)')
    op.execute('CREATE INDEX idx_test_case_project ON test_cases(project_id)')
    op.execute('CREATE INDEX idx_project_owner ON projects(owner_id)')
    op.execute('CREATE INDEX idx_execution_created ON executions(created_at DESC)')
    op.execute('CREATE INDEX idx_test_case_type ON test_cases(test_type)')
    op.execute('CREATE INDEX idx_execution_project ON executions(project_id)')

def downgrade() -> None:
    op.execute('DROP INDEX IF EXISTS idx_execution_status')
    op.execute('DROP INDEX IF EXISTS idx_test_case_project')
    op.execute('DROP INDEX IF EXISTS idx_project_owner')
    op.execute('DROP INDEX IF EXISTS idx_execution_created')
    op.execute('DROP INDEX IF EXISTS idx_test_case_type')
    op.execute('DROP INDEX IF EXISTS idx_execution_project')
