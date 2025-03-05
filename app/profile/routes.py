from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from datetime import datetime
from bson import ObjectId
from db.connection import get_db  # Import get_db instead of mongo
from app.utils import is_logged_in, get_current_user_id, get_current_user

profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/profile")
def profile():
    if not is_logged_in():
        return redirect(url_for("auth.login"))
    user = get_current_user()
    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    db = get_db()  # Get the database connection
    tasks = list(db.tasks.find({"user_id": str(user["_id"])}))  # Use db instead of mongo

    # Calculate task statistics
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.get("completed", False))
    on_time_tasks = sum(1 for task in tasks if
                      task.get("completed", False) and
                      task.get("completed_date") and
                      task.get("due_date") and
                      task["completed_date"] <= task["due_date"])

    cabin_pressure = round((on_time_tasks / completed_tasks * 100) if completed_tasks > 0 else 0)

    high_priority_tasks = sum(1 for task in tasks if task.get("priority") == "high-priority")
    medium_priority_tasks = sum(1 for task in tasks if task.get("priority") == "medium-priority")
    low_priority_tasks = sum(1 for task in tasks if task.get("priority") == "low-priority")

    current_date = datetime.now()
    overdue_tasks = sum(1 for task in tasks if
                     not task.get("completed", False) and
                     task.get("due_date") and
                     task["due_date"] < current_date)

    return render_template(
        'profile.html',
        active_page='profile',
        user=user,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        on_time_tasks=on_time_tasks,
        cabin_pressure=cabin_pressure,
        high_priority_tasks=high_priority_tasks,
        medium_priority_tasks=medium_priority_tasks,
        low_priority_tasks=low_priority_tasks,
        overdue_tasks=overdue_tasks
    )


@profile_bp.route("/get_current_user_info")
def get_current_user_info():
    if not is_logged_in():
        return jsonify({"error": "User not logged in"}), 401

    db = get_db()  # Get the database connection
    user = db.users.find_one({"_id": ObjectId(get_current_user_id())})  # Use db instead of mongo

    if user:
        tasks = list(db.tasks.find({"user_id": str(user["_id"])}))  # Use db instead of mongo
        
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.get("completed", False))
        on_time_tasks = sum(1 for task in tasks if
                            task.get("completed", False) and
                            task.get("completed_date") and
                            task.get("due_date") and
                            task["completed_date"] <= task["due_date"])
        
        cabin_pressure = round((on_time_tasks / completed_tasks * 100) if completed_tasks > 0 else 0)
        
        high_priority_tasks = sum(1 for task in tasks if task.get("priority") == "high-priority")
        medium_priority_tasks = sum(1 for task in tasks if task.get("priority") == "medium-priority")
        low_priority_tasks = sum(1 for task in tasks if task.get("priority") == "low-priority")
        
        current_date = datetime.now()
        overdue_tasks = sum(1 for task in tasks if
                            not task.get("completed", False) and
                            task.get("due_date") and
                            task["due_date"] < current_date)
        
        user_data = {
            "_id": str(user["_id"]),
            "username": user["username"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "points": user.get("points", 0),
            "streak_days": user.get("streak_days", 0),
            "streak_weeks": user.get("streak_weeks", 0),
            "achievements": user.get("achievements", []),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "on_time_tasks": on_time_tasks,
            "cabin_pressure": cabin_pressure,
            "high_priority_tasks": high_priority_tasks,
            "medium_priority_tasks": medium_priority_tasks,
            "low_priority_tasks": low_priority_tasks,
            "overdue_tasks": overdue_tasks
        }
        
        return jsonify(user_data)

    return jsonify({"error": "User not found"}), 404