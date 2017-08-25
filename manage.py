from flaskcasts import *
#from mimesis import Text, Personal
from flaskcasts.models import User

with app.app_context():
    eddiegrey = User('eddiegrey',
                     'eddie.sherman@gmail.com',
                     'password',
                     'Eddie Sherman')

    eddiegrey.save()
