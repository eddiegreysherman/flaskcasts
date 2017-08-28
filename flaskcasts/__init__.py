from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "1234567890987654321"

mongo = PyMongo(app)

from .views.home import home
app.register_blueprint(home)
