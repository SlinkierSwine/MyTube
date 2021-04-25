from application import app, api
from data import db_session, views
from api.video_resources import VideoResource
from api.user_resources import *

if __name__ == '__main__':
    db_session.global_init("db/videos.db")
    api.add_resource(VideoResource, '/api/video/<int:video_id>')
    api.add_resource(RegisterResource, '/api/register')
    api.add_resource(LoginResource, '/api/login')
    app.run()
