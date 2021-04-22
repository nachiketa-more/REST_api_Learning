from werkzeug.security import safe_str_cmp
from models.user_model import UserModel
# Registered users table
# Assume that below list as users table in Db
# users = [
#     User(1,'nmore','abcd'),
#     User(2,'pnikam', 'xyz')
#
# ]
#
# # Then we have User name mapping
# username_mapping = {u.username:u for u in users} # Set comprihension
#
#
# # Then we have user id mapping
# userid_mapping = {u.id:u for u in users}

# Tool functions
# 1. Authenticate User
#   Given a user name and password and selects correct user name form our list/table


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_userid(user_id)

