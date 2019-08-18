from sql import *
import config
from mongoengine import errors

admins = config.ADMINS

# add initial admins
try:
    for username, user_id in admins.items():
        Users(user_id=user_id, username=username, role=2).save()
        print('{0} was added as an admin'.format(username))
except errors.NotUniqueError:
    print("user already added")

