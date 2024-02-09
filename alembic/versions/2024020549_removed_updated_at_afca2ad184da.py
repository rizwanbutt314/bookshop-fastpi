"""removed updated_at

Revision ID: afca2ad184da
Revises: 290e56ed957d
Create Date: 2024-02-05 17:49:35.636298

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "afca2ad184da"
down_revision = "290e56ed957d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("author", "updated_at")
    op.drop_column("user", "updated_at")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "author",
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
    )
    # ### end Alembic commands ###
