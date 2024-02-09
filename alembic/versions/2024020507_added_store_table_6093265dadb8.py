"""Added store table

Revision ID: 6093265dadb8
Revises: 045946dff1a1
Create Date: 2024-02-05 20:07:38.175731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6093265dadb8"
down_revision = "045946dff1a1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "stores",
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=True),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["books.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("stores")
    # ### end Alembic commands ###
