# /backend/alembic/versions/20240326_add_is_email_verified_to_users.py

"""add is_email_verified column to users

Revision ID: 20240326_add_is_email_verified_to_users
Revises: <your_previous_revision_id>
Create Date: 2025-03-26

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20240326_add_is_email_verified_to_users"
down_revision = "ce2eb894601a"

branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "is_email_verified", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
    )


def downgrade():
    op.drop_column("users", "is_email_verified")
