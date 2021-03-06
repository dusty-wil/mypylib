"""initial setup

Revision ID: 042cad539f68
Revises: 
Create Date: 2020-03-10 21:55:33.957130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '042cad539f68'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('author', sa.String(length=64), nullable=False),
    sa.Column('isbn', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_book_author'), 'book', ['author'], unique=False)
    op.create_index(op.f('ix_book_isbn'), 'book', ['isbn'], unique=True)
    op.create_index(op.f('ix_book_title'), 'book', ['title'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('registration_date', sa.DateTime(), nullable=False),
    sa.Column('verified_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_registration_date'), 'user', ['registration_date'], unique=False)
    op.create_index(op.f('ix_user_verified_date'), 'user', ['verified_date'], unique=False)
    op.create_table('user_books',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('purch_date', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.String(length=1024), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'book_id')
    )
    op.create_index(op.f('ix_user_books_purch_date'), 'user_books', ['purch_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_books_purch_date'), table_name='user_books')
    op.drop_table('user_books')
    op.drop_index(op.f('ix_user_verified_date'), table_name='user')
    op.drop_index(op.f('ix_user_registration_date'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_book_title'), table_name='book')
    op.drop_index(op.f('ix_book_isbn'), table_name='book')
    op.drop_index(op.f('ix_book_author'), table_name='book')
    op.drop_table('book')
    # ### end Alembic commands ###
