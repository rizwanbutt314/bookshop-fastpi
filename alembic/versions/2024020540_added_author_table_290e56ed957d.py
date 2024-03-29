"""Added author table

Revision ID: 290e56ed957d
Revises: 07c71f4389b6
Create Date: 2024-02-05 17:40:11.989100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "290e56ed957d"
down_revision = "07c71f4389b6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "author",
        sa.Column("name", sa.String(length=254), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=False),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_author_name"), "author", ["name"], unique=True)
    op.create_table(
        "user",
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("hashed_password", sa.String(length=128), nullable=False),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.drop_index("ix_user_model_email", table_name="user_model")
    op.drop_table("user_model")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_model",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("email", sa.VARCHAR(length=254), autoincrement=False, nullable=False),
        sa.Column(
            "hashed_password",
            sa.VARCHAR(length=128),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="user_model_pkey"),
    )
    op.create_index("ix_user_model_email", "user_model", ["email"], unique=False)
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_author_name"), table_name="author")
    op.drop_table("author")
    # ### end Alembic commands ###
