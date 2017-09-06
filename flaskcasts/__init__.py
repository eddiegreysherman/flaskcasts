from flask import Flask
from flask_pymongo import PyMongo
import os

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

mongo = PyMongo(app)

from .views.home import home
app.register_blueprint(home)
