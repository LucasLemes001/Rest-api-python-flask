"""empty message

Revision ID: f583ae7a38da
Revises: 
Create Date: 2023-10-18 12:28:41.875365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f583ae7a38da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('BLOCKLIST',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('revoked_token', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('revoked_token')
    )
    op.create_table('lojas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('preco', sa.Float(precision=2), nullable=False),
    sa.Column('id_loja', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_loja'], ['lojas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=80), nullable=False),
    sa.Column('id_loja', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_loja'], ['lojas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('items_tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_item', sa.Integer(), nullable=True),
    sa.Column('id_tag', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_item'], ['items.id'], ),
    sa.ForeignKeyConstraint(['id_tag'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items_tags')
    op.drop_table('tags')
    op.drop_table('items')
    op.drop_table('users')
    op.drop_table('lojas')
    op.drop_table('BLOCKLIST')
    # ### end Alembic commands ###
