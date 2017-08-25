from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('config')

mongo = PyMongo(app)

from .views.home import home
app.register_blueprint(home)
