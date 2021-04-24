import sqlalchemy
from sqlalchemy import orm
from ..db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Video(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'videos'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    file_name = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    preview = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    rater = orm.relation("Rating",
                          backref="video_liked")
