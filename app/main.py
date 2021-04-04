from application import app
from data import db_session, views

if __name__ == '__main__':
    db_session.global_init("db/videos.db")
    app.run()
