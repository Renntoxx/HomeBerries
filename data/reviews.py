import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase

class Review(SqlAlchemyBase):
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                nullable=False)
    review = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_at = sqlalchemy.Column(sqlalchemy.Integer,
                                     default=datetime.datetime.now)
