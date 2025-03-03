from bson.objectid import ObjectId

# Sample users with total points tracking
sample_users = [
    {
        "_id": ObjectId(),
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "username": "alicej",
        "password": "hashed_password_1",
        "total_points": 100  # Tracks accumulated points from completed tasks
    },
    {
        "_id": ObjectId(),
        "name": "Bob Smith",
        "email": "bob@example.com",
        "username": "bobsmith",
        "password": "hashed_password_2",
        "total_points": 50
    }
]

# Sample priorities with point values
sample_priorities = [
    {
        "_id": ObjectId(),
        "name": "High",
        "point_value": 100,
        "rarity": "Common"
    },
    {
        "_id": ObjectId(),
        "name": "Medium",
        "point_value": 50,
        "rarity": "Uncommon"
    },
    {
        "_id": ObjectId(),
        "name": "Low",
        "point_value": 10,
        "rarity": "Rare"
    }
]

# Sample tasks with points tracking
sample_tasks = [
    {
        "_id": ObjectId(),
        "name": "Finish project",
        "priority_id": sample_priorities[0]["_id"],
        "completed": True,  # Task is completed
        "points_earned": 100,  # Earned points based on priority level
        "description": "Complete the final project report",
        "due_date": "2025-03-01",
        "task_type": "Work",
        "user_id": sample_users[0]["_id"]
    },
    {
        "_id": ObjectId(),
        "name": "Grocery shopping",
        "priority_id": sample_priorities[1]["_id"],
        "completed": True,  # Task is completed
        "points_earned": 50,  # Earned points
        "description": "Buy milk, eggs, and bread",
        "due_date": "2025-02-20",
        "task_type": "Personal",
        "user_id": sample_users[1]["_id"]
    },
    {
        "_id": ObjectId(),
        "name": "Read a book",
        "priority_id": sample_priorities[2]["_id"],
        "completed": False,  # Task is still pending
        "points_earned": 0,  # No points since it's not completed
        "description": "Read 50 pages of a book",
        "due_date": "2025-03-05",
        "task_type": "Leisure",
        "user_id": sample_users[0]["_id"]
    }
]
