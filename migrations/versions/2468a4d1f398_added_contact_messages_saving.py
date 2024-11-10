"""added contact messages saving

Revision ID: 2468a4d1f398
Revises: 12fdbf498e8d
Create Date: 2024-11-05 23:45:05.945290

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2468a4d1f398"
down_revision = "12fdbf498e8d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "contact_message",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("contact_message")
    # ### end Alembic commands ###