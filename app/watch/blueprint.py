from flask import Blueprint, abort, render_template, request, json
from data import db_session
from data.models.video import Video
from data.models.user import User
from data.models.rating import Rating
from data.models.association_tables import user_rate_video
import os
from flask_login import current_user


watch_blueprint = Blueprint(
    'watch',
    __name__,
    template_folder='templates'
)


def is_liked(video_id):
    db_sess = db_session.create_session()
    query_user_liked = db_sess.query(Video).join(Rating).join(User).filter(
        (Rating.user_rate_id == User.id) & (Rating.video_rate_id == Video.id) & (
                    User.id == current_user.id) & (Video.id == video_id)).first()
    if query_user_liked:
        return True
    return False


def is_disliked(video_id):
    db_sess = db_session.create_session()
    query_dislikes = db_sess.query(Video).join(user_dislike_video).join(User).filter(
         (User.id == current_user.id) & (Video.id == video_id)).first()
    if query_dislikes:
        return True
    return False


@watch_blueprint.route('/<int:video_id>')
def show_video(video_id):
    pathsep = os.path.sep
    db_sess = db_session.create_session()
    video = db_sess.query(Video).get(video_id)
    if not video:
        abort(404)
    else:
        author = db_sess.query(User).get(video.user_id)
        return render_template('player.html', video=video, author=author, pathsep=pathsep, title=f'MyTube: {video.title}')


@watch_blueprint.route('/_is_rated')
def json_is_rated():
    video_id = request.args.get('video_id', 0, type=int)
    liked = is_liked(video_id)
    disliked = is_disliked(video_id)
    return json.dumps({'is_liked': liked, 'is_disliked': disliked})


@watch_blueprint.route('/_like')
def like():
    db_sess = db_session.create_session()
    video_id = request.args.get('video_id', 0, type=int)
    liked = is_liked(video_id)
    disliked = is_disliked(video_id)
    if not liked:
        if disliked:
            remove_dislike(video_id)
        video = db_sess.query(Video).filter(Video.id == video_id).first()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        rating = Rating(like_or_dislike=1)
        video.likers.append(user, like_or_dislike=1)
        user.liked.append(video, like_or_dislike=1)
        db_sess.commit()
    elif liked:
        remove_like(video_id)
    return json.dumps({'is_liked': liked})


def remove_like(video_id):
    db_sess = db_session.create_session()
    video = db_sess.query(Video).filter(Video.id == video_id).first()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    video.likers.remove(user)
    db_sess.commit()


@watch_blueprint.route('/_dislike')
def dislike():
    db_sess = db_session.create_session()
    video_id = request.args.get('video_id', 0, type=int)
    liked = is_liked(video_id)
    disliked = is_disliked(video_id)
    if not disliked:
        if liked:
            remove_like(video_id)
        video = db_sess.query(Video).filter(Video.id == video_id).first()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        video.dislikers.append(user)
        user.disliked.append(video)
        db_sess.commit()
    elif disliked:
        remove_dislike(video_id)
    return json.dumps({'is_disliked': disliked})


def remove_dislike(video_id):
    db_sess = db_session.create_session()
    video = db_sess.query(Video).filter(Video.id == video_id).first()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    video.dislikers.remove(user)
    db_sess.commit()


@watch_blueprint.route('/_count_rates')
def json_count_rates():
    db_sess = db_session.create_session()
    video_id = request.args.get('video_id', 0, type=int)
    query_count_likes = db_sess.query(Video).join(user_like_video).join(User).filter(Video.id == video_id).count()
    query_count_dislikes = db_sess.query(Video).join(user_dislike_video).join(User).filter(Video.id == video_id).count()
    return json.dumps({'likes': query_count_likes, 'dislikes': query_count_dislikes})


@watch_blueprint.route('/_count_likes')
def json_count_likes():
    db_sess = db_session.create_session()
    video_id = request.args.get('video_id', 0, type=int)
    query_likes = db_sess.query(Video).join(Rating).join(User).filter(
        (Rating.user_rate_id == User.id) & (Rating.video_rate_id == Video.id) & (Video.id == video_id)).count()
    return json.dumps({'likes': query_likes})
