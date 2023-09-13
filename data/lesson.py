import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Lesson(SqlAlchemyBase):
    __tablename__ = 'week'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    first = sqlalchemy.Column(sqlalchemy.String)
    second = sqlalchemy.Column(sqlalchemy.String)
    third = sqlalchemy.Column(sqlalchemy.String)
    fourth = sqlalchemy.Column(sqlalchemy.String)
    fifth = sqlalchemy.Column(sqlalchemy.String)
    sixth = sqlalchemy.Column(sqlalchemy.String)
    seventh = sqlalchemy.Column(sqlalchemy.String)
