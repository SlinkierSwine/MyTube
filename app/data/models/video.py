import sqlalchemy
from sqlalchemy import orm
from ..db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Video(SqlAlchemyBase, SerializerMixin):
    """Модель видео"""
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
    likes_count = sqlalchemy.Column(sqlalchemy.Integer)
    dislikes_count = sqlalchemy.Column(sqlalchemy.Integer)

    user = orm.relation('User')

    likers = orm.relation("User",
                         secondary='likes',
                         backref="video_liked")
    dislikers = orm.relation("User",
                         secondary='dislikes',
                         backref="video_disliked")
