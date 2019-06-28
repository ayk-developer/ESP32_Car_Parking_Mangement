from flask import Flask
from flask_login import LoginManager
from app.carcounter import carcounter
carcounter=carcounter()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
from app import routes
