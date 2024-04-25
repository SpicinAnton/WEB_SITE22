import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase


class Tovar(SqlAlchemyBase):
    __tablename__ = 'tovars'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)


    def __repr__(self):
        return f'<Tovar> {self.id} {self.name} {self.name1}'
