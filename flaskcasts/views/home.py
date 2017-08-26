from flask import Blueprint, render_template, request
from flaskcasts import mongo
from flask_pymongo import pymongo
from flaskcasts.common.pagination import paginate

home = Blueprint('home', __name__)

@home.route('/')
def index():
    page = int((request.args.get('page') or 1))
    posts = mongo.db.posts.find().sort('created', pymongo.DESCENDING)
    paginated_posts = paginate(posts, page, per_page=5)
    return render_template('home/index.html',
                           paginated_posts=paginated_posts)

