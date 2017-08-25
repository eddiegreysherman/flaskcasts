from flaskcasts import *
from mimesis import Text, Personal
from flaskcasts.models import User, Post
en = Text('en')

# with app.app_context():
#     eddiegrey = User('eddiegrey',
#                      'eddie.sherman@gmail.com',
#                      'password',
#                      'Eddie Sherman')
#
#     eddiegrey.save()

with app.app_context():
    for i in range(20):
        post = Post(en.sentence(), en.text(), 'eddiegrey')
        post.save()