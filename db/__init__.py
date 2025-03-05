from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    """
    Initialize the MongoDB connection with the Flask app.
    """
    mongo.init_app(app)
    print("✅ Database initialized!")