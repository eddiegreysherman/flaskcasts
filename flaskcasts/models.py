import datetime
import uuid

from flaskcasts import mongo
from slugify import slugify
from flask_pymongo import pymongo

##########################
#                        #
#                        #
#       Users Model      #
#                        #
#                        #
##########################
class User(object):

    def __init__(self, _id, email, password, fullname):
        self._id = _id # username, unique
        self.email = email
        self.password = password
        self.fullname = fullname

    def __repr__(self):
        return "<User {}>".format(self.fullname)

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "fullname": self.fullname
        }

    @staticmethod
    def get_user(user_id):
        return mongo.db.users.find_one({"_id": user_id})

    def save(self):
        mongo.db.users.update({"_id": self._id}, self.json(), upsert=True)


##########################
#                        #
#                        #
#       Posts Model      #
#                        #
#                        #
##########################

class Post(object):


    def __init__(self, title, content, author, created=None):
        self._id = uuid.uuid4().hex
        self.title = title
        self.slug = slugify(title)
        self.content = content
        self.author = author
        self.created = datetime.datetime.utcnow().strftime('%A %x @ %H:%M:%S') \
            if created is None else created

    def __repr__(self):
        return "<Post {}>".format(self.title)

    def json(self):
        return {
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "author": self.author,
            "created": self.created
        }

    @staticmethod
    def all_desc():
        return mongo.db.posts.find().sort('created', pymongo.DESCENDING)

    @staticmethod
    def get_post(key, val):
        return mongo.db.posts.find_one({key: val})

    def save(self):
        mongo.db.posts.update({'slug': self.slug}, self.json(), upsert=True)


