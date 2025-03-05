from flask import session
from bson.objectid import ObjectId
from app import mongo  # Import mongo from app/__init__.py

def is_logged_in():
    return "user_id" in session

def get_current_user_id():
    return session.get("user_id")

def get_current_user():
    if not is_logged_in():
        return None
    return mongo.db.users.find_one({"_id": ObjectId(get_current_user_id())})

def check_achievements(user):
    # Your existing check_achievements logic
    pass