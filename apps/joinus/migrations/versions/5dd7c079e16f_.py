"""empty message

Revision ID: 5dd7c079e16f
Revises: c1e96ed0d2e9
Create Date: 2016-08-27 11:40:14.457225

"""

# revision identifiers, used by Alembic.
revision = '5dd7c079e16f'
down_revision = 'c1e96ed0d2e9'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('applicant_ibfk_3', 'applicant', type_='foreignkey')
    op.drop_column('applicant', 'user_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('applicant', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('applicant_ibfk_3', 'applicant', 'user', ['user_id'], ['id'])
    ### end Alembic commands ###
