from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_ngrok import run_with_ngrok


app = Flask(__name__)
app.config.from_object(Config)
run_with_ngrok(app)

login_manager = LoginManager()
login_manager.init_app(app)
