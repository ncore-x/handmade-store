"""change admin model

Revision ID: af89feea9d7b
Revises: 96290dedc1f5
Create Date: 2025-10-26 21:27:18.850099

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "af89feea9d7b"
down_revision: Union[str, Sequence[str], None] = "96290dedc1f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("admins", "is_active")
    op.drop_column("admins", "permissions")
    op.drop_column("admins", "is_superuser")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "admins",
        sa.Column("is_superuser", sa.BOOLEAN(),
                  autoincrement=False, nullable=False),
    )
    op.add_column(
        "admins",
        sa.Column(
            "permissions",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "admins",
        sa.Column("is_active", sa.BOOLEAN(),
                  autoincrement=False, nullable=False),
    )
