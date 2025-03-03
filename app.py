from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask_mail import Mail, Message

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set configurations
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your_strong_secret_key_here")
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/task_manager")

# Initialize MongoDB connection
mongo = PyMongo(app)

# Configure Flask-Mail for password reset emails
app.config["MAIL_SERVER"] = "smtp.example.com"  # Use a real SMTP server
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)

# Helper function to check if a user is logged in
def is_logged_in():
    return "user_id" in session

# Helper function to check if a user is logged in
def is_logged_in():
    return "user_id" in session


# Helper function to get the current user's ID
def get_current_user_id():
    return session.get("user_id")

# Helper function to get the current user's document
def get_current_user():
    if not is_logged_in():
        return None
    return mongo.db.users.find_one({"_id": ObjectId(get_current_user_id())})

# Function to check and award achievements
def check_achievements(user):
    user_id = user["_id"]
    achievements = user.get("achievements", [])
    tasks = list(mongo.db.tasks.find({"user_id": str(user_id), "completed": True}))

    # First Task Completed
    if len(tasks) == 1 and "First Task Completed" not in achievements:
        achievements.append("First Task Completed")
        flash("Achievement Unlocked: First Task Completed!", "success")

    # Task Master
    if len(tasks) >= 10 and "Task Master" not in achievements:
        achievements.append("Task Master")
        flash("Achievement Unlocked: Task Master!", "success")

    # Streak Starter
    if user.get("streak_days", 0) >= 3 and "Streak Starter" not in achievements:
        achievements.append("Streak Starter")
        flash("Achievement Unlocked: Streak Starter!", "success")

    # Weekend Warrior
    if datetime.now().weekday() in [5, 6]:  # Saturday (5) or Sunday (6)
        weekend_tasks = list(mongo.db.tasks.find({"user_id": str(user_id), "completed": True, "completed_date": {"$gte": datetime.now() - timedelta(days=2)}}))
        if len(weekend_tasks) >= 2 and "Weekend Warrior" not in achievements:
            achievements.append("Weekend Warrior")
            flash("Achievement Unlocked: Weekend Warrior!", "success")

    # High Priority Hero
    high_priority_tasks = list(mongo.db.tasks.find({"user_id": str(user_id), "completed": True, "priority": "high-priority"}))
    if len(high_priority_tasks) >= 5 and "High Priority Hero" not in achievements:
        achievements.append("High Priority Hero")
        flash("Achievement Unlocked: High Priority Hero!", "success")

    # Update user achievements
    mongo.db.users.update_one(
        {"_id": user_id},
        {"$set": {"achievements": achievements}},
    )

# Routes
@app.route("/")
def index():
    return render_template("index.html")


# Signup Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        confirm_password = request.form.get("confirm_password")
        email = request.form.get("email")

        if not (username and first_name and last_name and password and confirm_password and email):
            flash("All fields are required.", "error")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        existing_user = mongo.db.users.find_one({"$or": [{"username": username}, {"email": email}]})
        if existing_user:
            flash("User already exists.", "error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        user_data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": hashed_password,
            "email": email,
            "points": 0,
            "streak_days": 0,
            "streak_weeks": 0,
            "last_completed": None,
            "achievements": [],
        }
        mongo.db.users.insert_one(user_data)

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# Login Route (Allows Login with Either Username or Email)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = mongo.db.users.find_one({"$or": [{"username": username}, {"email": username}]})

        if user and check_password_hash(user["password"], password):
            session["user_id"] = str(user["_id"])  # Store user_id as a string
            return redirect(url_for("home"))

        flash("Invalid username or password", "error")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/home")
def home():
    if not is_logged_in():
        return redirect(url_for("login"))

    user = get_current_user()
    if not user:
        session.clear()
        return redirect(url_for("login"))

    # Fixed: Changed ObjectId(user["_id"]) to str(user["_id"]) to match storage format
    tasks = list(mongo.db.tasks.find({"user_id": str(user["_id"])}))
    
    # Debug output
    print(f"User ID: {str(user['_id'])}")
    print(f"Found {len(tasks)} tasks for user")
    
    overdue_tasks = sum(1 for task in tasks if task.get("due_date") and task["due_date"] < datetime.now())
    completed_tasks_today = sum(1 for task in tasks if task.get("completed") and task.get("completed_date") == datetime.now().date())

    return render_template(
        "home.html",
        username=user["username"],
        tasks=tasks,
        overdue_tasks=overdue_tasks,
        completed_tasks_today=completed_tasks_today,
        total_points=user.get("points", 0),
        streak_days=user.get("streak_days", 0),
        streak_weeks=user.get("streak_weeks", 0),
        achievements=user.get("achievements", []),
    )

@app.route("/contact")
def contact():
    return render_template('contact-us.html', active_page='contact')

@app.route("/add-task", methods=["POST"])
def add_task():
    if not is_logged_in():
        return redirect(url_for("login"))

    user_id = get_current_user_id()
    task = request.form.get("task")
    priority = request.form.get("priority", "low-priority")  # Default to "low-priority"

    # Debug output
    print(f"Adding task: {task} with priority {priority} for user {user_id}")

    # Fetch the priority document to get its ID
    priority_doc = mongo.db.priorities.find_one({"name": priority})
    priority_id = str(priority_doc["_id"]) if priority_doc else None

    # Store user_id as string to match query format
    mongo.db.tasks.insert_one(
        {
            "user_id": str(user_id),  # Explicitly store as string
            "task": task,
            "priority": priority,
            "priority_id": priority_id,  # Add priority_id
            "completed": False,
            "due_date": datetime.now() + timedelta(days=7),  # Example: Set due date to 7 days from now
        }
    )

    return "", 204  # Return an empty response with status code 204 (No Content)

@app.route("/update-task/<task_id>", methods=["POST"])
def update_task(task_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    updated_task = request.form.get("task")
    priority = request.form.get("priority", "low-priority")  # Default to "low-priority" if not provided

    # Debug output
    print(f"Updating task {task_id}: {updated_task} with priority {priority}")

    mongo.db.tasks.update_one(
        {"_id": ObjectId(task_id), "user_id": str(get_current_user_id())},  # Match user_id as string
        {"$set": {"task": updated_task, "priority": priority}},
    )

    return "", 204  # Return an empty response with status code 204 (No Content)

@app.route("/delete-task/<task_id>", methods=["POST"])
def delete_task(task_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    # Debug output
    print(f"Deleting task {task_id}")

    mongo.db.tasks.delete_one({"_id": ObjectId(task_id), "user_id": str(get_current_user_id())})  # Match user_id as string
    return "", 204  # Return an empty response with status code 204 (No Content)

@app.route("/toggle-completion/<task_id>", methods=["POST"])
def toggle_completion(task_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    # Find the task with string user_id
    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id), "user_id": str(get_current_user_id())})
    
    # Debug output
    print(f"Toggling completion for task {task_id}: {task}")
    
    if task:
        completed = not task.get("completed", False)
        
        # Check if priority_id exists and is valid
        if "priority_id" in task and task["priority_id"]:
            try:
                priority = mongo.db.priorities.find_one({"_id": ObjectId(task["priority_id"])})
                point_value = priority["point_value"] if priority else 0
            except:
                # Fallback for invalid priority_id
                point_value = 0
        else:
            # Default point values based on priority string
            priority_values = {
                "high-priority": 5,
                "medium-priority": 3,
                "low-priority": 1
            }
            point_value = priority_values.get(task.get("priority"), 0)

        mongo.db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {
                "$set": {
                    "completed": completed,
                    "completed_date": datetime.now() if completed else None,
                    "points_earned": point_value if completed else 0,
                }
            },
        )

        if completed:
            user = mongo.db.users.find_one({"_id": ObjectId(get_current_user_id())})
            mongo.db.users.update_one(
                {"_id": ObjectId(get_current_user_id())},
                {"$inc": {"points": point_value}},
            )

            # Check for achievements
            check_achievements(user)

    return "", 204  # Return an empty response with status code 204 (No Content)

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logged out. See you soon!", "info")
    return redirect('/')

# Forgot Password Route
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = mongo.db.users.find_one({"email": email})

        if user:
            reset_token = secrets.token_urlsafe(32)
            mongo.db.users.update_one({"_id": user["_id"]}, {"$set": {"reset_token": reset_token}})

            reset_url = url_for("reset_password", token=reset_token, _external=True)
            msg = Message("Password Reset Request", sender="noreply@example.com", recipients=[email])
            msg.body = f"Click the link to reset your password: {reset_url}"
            mail.send(msg)

            flash("Check your email for reset instructions.", "success")
            return redirect(url_for("login"))

    return render_template("forgot_password.html")

# Reset Password Route
@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = mongo.db.users.find_one({"reset_token": token})

    if not user:
        return render_template("reset_password.html", message="Invalid or expired token.")

    if request.method == "POST":
        new_password = request.form.get("password")
        hashed_password = generate_password_hash(new_password)
        mongo.db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"password": hashed_password, "reset_token": None}},
        )
        return redirect(url_for("login"))

    return render_template("reset_password.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)