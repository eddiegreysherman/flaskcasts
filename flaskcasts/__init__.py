from flask import Flask
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

mongo = PyMongo(app)

from .views.home import home
app.register_blueprint(home)
