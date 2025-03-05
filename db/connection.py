from pymongo import MongoClient

# Function to get the MongoDB database
def get_db():
    client = MongoClient("mongodb://localhost:27017")
    return client["task_manager"]