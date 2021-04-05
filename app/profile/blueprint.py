from flask import Blueprint, abort, render_template
from data import db_session
from data.models.video import Video
from data.models.user import User


profile_blueprint = Blueprint(
    'profile',
    __name__,
    template_folder='templates'
)


@profile_blueprint.route('/<int:user_id>')
def profile(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        abort(404)
    else:
        videos = db_sess.query(Video).filter(Video.user_id == user_id)
        return render_template('profile.html', user=user, videos=videos)
