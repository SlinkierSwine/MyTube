from application import app, api
from data import db_session, views
from api.video_resources import VideoResource
from api.user_resources import *
import os

if __name__ == '__main__':
    if not os.path.isdir(app.config['DB_FOLDER']):
        os.mkdir(app.config['DB_FOLDER'])
    db_session.global_init(app.config['DB_PATH'])

    api.add_resource(VideoResource, '/api/video/<int:video_id>')
    api.add_resource(RegisterResource, '/api/register')
    api.add_resource(LoginResource, '/api/login')

    app.run()
