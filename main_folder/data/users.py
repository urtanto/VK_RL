import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    vk = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    money = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    profession = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    zarplata = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    home = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    garage = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cars = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    education = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    last_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ban = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    role = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    working = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    learning = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    keyboard = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    now = sqlalchemy.Column(sqlalchemy.String, nullable=True)
