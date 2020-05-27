import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    vk_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    enter = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    money = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    profession = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    zarplata = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)