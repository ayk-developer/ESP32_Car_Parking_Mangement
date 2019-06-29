from flask import Flask
from flask_apscheduler import APScheduler
from flask_login import LoginManager
from app.carcounter import carcounter
carcounter=carcounter()

def cutbill1():
    carcounter.cutbill()

app = Flask(__name__)
scheduler = APScheduler()
# it is also possible to enable the API directly
# scheduler.api_enabled = True

scheduler.init_app(app)
scheduler.start()
app.apscheduler.add_job(id='job1',func=cutbill1, trigger='interval', seconds= 600)
app.config['SECRET_KEY'] = 'you-will-never-guess'
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
from app import routes
