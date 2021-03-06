import datetime
import uuid
from flaskcasts import mongo
from slugify import slugify
from flask_pymongo import pymongo
from flaskcasts.common.utils import Utils
import flaskcasts.common.user_errors as UserError

##########################
#                        #
#                        #
#       Users Model      #
#                        #
#                        #
##########################


class User(object):

    def __init__(self, _id, email, password, fullname):
        self._id = _id  # username, unique
        self.email = email
        self.password = Utils.hash_password(password)
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
    def get_user(key, val):
        return mongo.db.users.find_one({key: val})

    @staticmethod
    def is_login_valid(user_id, password):
        user_data = mongo.db.users.find_one({"_id": user_id})
        if user_data is None:
            # Email doesn't exist.
            raise UserError.UserNotExistsError("User is not registered.")
        if not Utils.check_hashed_password(password, user_data['password']):
            # Password is incorrect.
            raise UserError.IncorrectPasswordError("Password is incorrect.")

        return True



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
        self.slug = slugify(title)  # we are linking to posts with this slug...needs uniqueness
        self.content = content
        self.author = author
        self.created = datetime.datetime.utcnow() \
            if created is None else created

    def __repr__(self):
        return "<Post {}>".format(self.title)

    def json(self):
        return {
            "_id": self._id,
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
        mongo.db.posts.update({'_id': self._id}, self.json(), upsert=True)

    @staticmethod
    def update(post_id, title, content):
        mongo.db.posts.update({'_id': post_id}, {'$set': {"title": title, "content": content}})

    @staticmethod
    def remove_post(post_id):
        post = mongo.db.posts.find_one({"_id": post_id})
        mongo.db.posts.remove(post)
