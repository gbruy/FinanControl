"""Adicionar tabela categorias e atualiza transacoes

Revision ID: dbad893c57b1
Revises: dbefb3cb895a
Create Date: 2025-02-05 16:52:32.606543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbad893c57b1'
down_revision = 'dbefb3cb895a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categoria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('transacao', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'categoria', ['categoria_id'], ['id'])
        batch_op.drop_column('categoria')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transacao', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('categoria_id')

    op.drop_table('categoria')
    # ### end Alembic commands ###
