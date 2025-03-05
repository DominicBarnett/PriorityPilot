from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from db.connection import get_db  # Use get_db for database connection
from app.utils import is_logged_in, get_current_user_id
from bson import ObjectId
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/home")
def home():
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    db = get_db()  # Get the database connection
    user_id = get_current_user_id()
    tasks = list(db.tasks.find({"user_id": user_id}))

    return render_template("tasks/home.html", tasks=tasks)


@tasks_bp.route("/add-task", methods=["POST"])
def add_task():
    if not is_logged_in():
        return jsonify({"error": "User not logged in"}), 401

    db = get_db()  # Get the database connection
    user_id = get_current_user_id()

    task_data = {
        "user_id": user_id,
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "priority": request.form.get("priority"),
        "due_date": datetime.strptime(request.form.get("due_date"), "%Y-%m-%d"),
        "completed": False,
        "created_at": datetime.now(),
        "completed_date": None,
    }

    db.tasks.insert_one(task_data)
    return jsonify({"message": "Task added successfully"}), 201


@tasks_bp.route("/update-task/<task_id>", methods=["POST"])
def update_task(task_id):
    if not is_logged_in():
        return jsonify({"error": "User not logged in"}), 401

    db = get_db()  # Get the database connection
    user_id = get_current_user_id()

    task = db.tasks.find_one({"_id": ObjectId(task_id), "user_id": user_id})
    if not task:
        return jsonify({"error": "Task not found"}), 404

    update_data = {
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "priority": request.form.get("priority"),
        "due_date": datetime.strptime(request.form.get("due_date"), "%Y-%m-%d"),
    }

    db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})
    return jsonify({"message": "Task updated successfully"}), 200


@tasks_bp.route("/delete-task/<task_id>", methods=["POST"])
def delete_task(task_id):
    if not is_logged_in():
        return jsonify({"error": "User not logged in"}), 401

    db = get_db()  # Get the database connection
    user_id = get_current_user_id()

    task = db.tasks.find_one({"_id": ObjectId(task_id), "user_id": user_id})
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.tasks.delete_one({"_id": ObjectId(task_id)})
    return jsonify({"message": "Task deleted successfully"}), 200


@tasks_bp.route("/toggle-completion/<task_id>", methods=["POST"])
def toggle_completion(task_id):
    if not is_logged_in():
        return jsonify({"error": "User not logged in"}), 401

    db = get_db()  # Get the database connection
    user_id = get_current_user_id()

    task = db.tasks.find_one({"_id": ObjectId(task_id), "user_id": user_id})
    if not task:
        return jsonify({"error": "Task not found"}), 404

    completed = not task.get("completed", False)
    completed_date = datetime.now() if completed else None

    db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"completed": completed, "completed_date": completed_date}},
    )
    return jsonify({"message": "Task completion toggled successfully"}), 200