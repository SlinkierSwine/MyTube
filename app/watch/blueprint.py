from flask import Blueprint, abort, render_template
from data import db_session
from data.models.video import Video
from data.models.user import User


watch_blueprint = Blueprint(
    'watch',
    __name__,
    template_folder='templates'
)


@watch_blueprint.route('/<int:video_id>')
def show_video(video_id):
    db_sess = db_session.create_session()
    video = db_sess.query(Video).get(video_id)
    author = db_sess.query(User).get(video.user_id)
    if not video:
        abort(404)
    else:
        return render_template('player.html', video=video, author=author)
