from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_ngrok import run_with_ngrok
from watch.blueprint import watch_blueprint
from account.blueprint import account_blueprint


app = Flask(__name__)
app.config.from_object(Config)
run_with_ngrok(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(watch_blueprint, url_prefix='/watch')
app.register_blueprint(account_blueprint, url_prefix='/account')
