import sqlalchemy
from ..db_session import SqlAlchemyBase


user_like_to_video = sqlalchemy.Table(
    'likes',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('video', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('videos.id')),
    sqlalchemy.Column('like_or_dislike', sqlalchemy.Integer)
)
