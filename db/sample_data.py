from bson.objectid import ObjectId

sample_users = [
    {"_id": ObjectId(), "name": "Alice Johnson", "email": "alice@example.com", "username": "alicej", "password": "hashed_password_1"},
    {"_id": ObjectId(), "name": "Bob Smith", "email": "bob@example.com", "username": "bobsmith", "password": "hashed_password_2"}
]

sample_priorities = [
    {"_id": ObjectId(), "name": "High", "point_value": 100, "rarity": "Common"},
    {"_id": ObjectId(), "name": "Medium", "point_value": 50, "rarity": "Uncommon"},
    {"_id": ObjectId(), "name": "Low", "point_value": 10, "rarity": "Rare"}
]

sample_tasks = [
    {"_id": ObjectId(), "name": "Finish project", "priority_id": sample_priorities[0]["_id"], "completed": False, "description": "Complete the final project report", "due_date": "2025-03-01", "task_type": "Work", "user_id": sample_users[0]["_id"]},
    {"_id": ObjectId(), "name": "Grocery shopping", "priority_id": sample_priorities[1]["_id"], "completed": False, "description": "Buy milk, eggs, and bread", "due_date": "2025-02-20", "task_type": "Personal", "user_id": sample_users[1]["_id"]}
]
