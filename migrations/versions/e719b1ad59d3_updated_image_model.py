"""Updated image model

Revision ID: e719b1ad59d3
Revises: f16749a74f3b
Create Date: 2024-11-15 23:24:29.316585

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "e719b1ad59d3"
down_revision = "f16749a74f3b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("images", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("image_source", sa.String(length=50), nullable=False)
        )
        batch_op.add_column(sa.Column("file_data", sa.LargeBinary(), nullable=True))
        batch_op.add_column(sa.Column("url", sa.String(length=255), nullable=True))
        batch_op.drop_column("data")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("images", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("data", postgresql.BYTEA(), autoincrement=False, nullable=False)
        )
        batch_op.drop_column("url")
        batch_op.drop_column("file_data")
        batch_op.drop_column("image_source")

    # ### end Alembic commands ###
