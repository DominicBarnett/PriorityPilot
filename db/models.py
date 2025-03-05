from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, name, email, username, password, _id=None):
        self.id = ObjectId(_id) if _id else None
        self.name = name
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)  # Hash the password

    def to_dict(self):
        return {
            "_id": str(self.id) if self.id else None,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "password": self.password
        }

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Task:
    def __init__(self, name, priority_id, completed, description, due_date, task_type, user_id, _id=None):
        self.id = ObjectId(_id) if _id else None
        self.name = name
        self.priority_id = ObjectId(priority_id) if priority_id else None
        self.completed = completed
        self.description = description
        self.due_date = due_date  # Ensure this is a datetime object
        self.task_type = task_type
        self.user_id = ObjectId(user_id) if user_id else None

    def to_dict(self):
        return {
            "_id": str(self.id) if self.id else None,
            "name": self.name,
            "priority_id": str(self.priority_id) if self.priority_id else None,
            "completed": self.completed,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "task_type": self.task_type,
            "user_id": str(self.user_id) if self.user_id else None
        }

class Priority:
    def __init__(self, name, point_value, rarity, _id=None):
        self.id = ObjectId(_id) if _id else None
        self.name = name
        self.point_value = point_value
        self.rarity = rarity

    def to_dict(self):
        return {
            "_id": str(self.id) if self.id else None,
            "name": self.name,
            "point_value": self.point_value,
            "rarity": self.rarity
        }