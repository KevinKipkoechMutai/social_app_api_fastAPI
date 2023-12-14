"""create post table

Revision ID: 3590c6d0c2a6
Revises: 2fe5ba05f9e3
Create Date: 2023-12-11 07:53:01.397813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3590c6d0c2a6'
down_revision: Union[str, None] = '2fe5ba05f9e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
