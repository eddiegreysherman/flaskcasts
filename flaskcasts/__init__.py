from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "Sup3rM4nK37"

mongo = PyMongo(app)

from .views.home import home
app.register_blueprint(home)
