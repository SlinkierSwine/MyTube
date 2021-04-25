import sqlalchemy
from ..db_session import SqlAlchemyBase


# Таблица связи пользователя, лайкнувшего видео
user_like_video = sqlalchemy.Table(
    'likes',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_liker', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('video_liked', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('videos.id'))
)

# Таблица связи пользователя, дизлайкнувшего видео
user_dislike_video = sqlalchemy.Table(
    'dislikes',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_disliker', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('video_disliked', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('videos.id'))
)

