import sqlalchemy
from ..db_session import SqlAlchemyBase


user_rate_video = sqlalchemy.Table(
    'likes',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_liker', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('video_liked', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('videos.id'))
)

user_dislike_video = sqlalchemy.Table(
    'dislikes',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_disliker', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('video_disliked', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('videos.id'))
)

