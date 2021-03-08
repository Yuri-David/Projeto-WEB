from flask import Flask
from flask_ngrok import run_with_ngrok
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
run_with_ngrok(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.controllers import default
from app.models import usuario
from app.models import estoque