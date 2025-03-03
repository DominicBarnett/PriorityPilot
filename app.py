from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from datetime import datetime, timedelta, time
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
    
    # Get the latest user data to ensure we have current streak information
    updated_user = mongo.db.users.find_one({"_id": user_id})
    streak_days = updated_user.get("streak_days", 0)

    # First Task Completed
    if len(tasks) == 1 and "First Task Completed" not in achievements:
        achievements.append("First Task Completed")
        flash("Achievement Unlocked: First Task Completed!", "success")

    # Task Master
    if len(tasks) >= 10 and "Task Master" not in achievements:
        achievements.append("Task Master")
        flash("Achievement Unlocked: Task Master!", "success")

    # Streak Starter - using the updated streak_days value
    if streak_days >= 3 and "Streak Starter" not in achievements:
        achievements.append("Streak Starter")
        flash("Achievement Unlocked: Streak Starter!", "success")

    # Weekend Warrior
    if datetime.now().weekday() in [5, 6]:  # Saturday (5) or Sunday (6)
        weekend_tasks = list(mongo.db.tasks.find({
            "user_id": str(user_id), 
            "completed": True, 
            "completed_date": {"$gte": datetime.now() - timedelta(days=2)}
        }))
        if len(weekend_tasks) >= 2 and "Weekend Warrior" not in achievements:
            achievements.append("Weekend Warrior")
            flash("Achievement Unlocked: Weekend Warrior!", "success")

    # High Priority Hero
    high_priority_tasks = list(mongo.db.tasks.find({
        "user_id": str(user_id), 
        "completed": True, 
        "priority": "high-priority"
    }))
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
    
    # FIX: Only count uncompleted tasks with due dates before today as overdue
    current_date = datetime.now()
    today_date = current_date.date()
    
    overdue_tasks = sum(1 for task in tasks if 
                     not task.get("completed", False) and 
                     task.get("due_date") and 
                     task["due_date"] < current_date)

    # IMPROVED: Count completed tasks today more accurately
    completed_tasks_today = sum(1 for task in tasks if 
                             task.get("completed", True) and 
                             task.get("completed_date") and 
                             isinstance(task["completed_date"], datetime) and
                             task["completed_date"].date() == today_date)

    print("overdue_tasks", overdue_tasks)
    print("completed_tasks_today", completed_tasks_today)
    
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
        active_page='home'
    )

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
            "due_date": datetime.combine(datetime.now().date(), time(23, 59, 59)) 
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
        current_time = datetime.now()
        
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

        # Update the task with completion status and timestamp
        update_data = {
            "completed": completed,
            "points_earned": point_value if completed else 0,
        }
        
        # Only set completed_date if task is marked as completed
        if completed:
            update_data["completed_date"] = current_time
        
        mongo.db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )

        if completed:
            user = mongo.db.users.find_one({"_id": ObjectId(get_current_user_id())})
            
            # Update streak logic
            today = current_time.date()
            last_completed = user.get("last_completed")
            streak_days = user.get("streak_days", 0)
            streak_weeks = user.get("streak_weeks", 0)
            
            if last_completed:
                last_completed_date = last_completed.date() if isinstance(last_completed, datetime) else last_completed
                # If completed yesterday, increase streak
                if (today - last_completed_date).days == 1:
                    streak_days += 1
                # If same day, don't change streak
                elif (today - last_completed_date).days == 0:
                    pass
                # If more than 1 day gap, reset streak
                else:
                    streak_days = 1
            else:
                # First time completing a task
                streak_days = 1
            
            # Update week streak if applicable (every 7 days)
            if streak_days % 7 == 0 and streak_days > 0:
                streak_weeks += 1
            
            # Update user with new streak information and points
            mongo.db.users.update_one(
                {"_id": ObjectId(get_current_user_id())},
                {
                    "$set": {
                        "last_completed": current_time,
                        "streak_days": streak_days,
                        "streak_weeks": streak_weeks
                    },
                    "$inc": {"points": point_value}
                },
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

@app.route("/sidebar")
def sidebar():
    return render_template('sidebar.html')

@app.route("/profile")
def profile():
    if not is_logged_in():
        return redirect(url_for("login"))
    
    user = get_current_user()
    if not user:
        session.clear()
        return redirect(url_for("login"))
    
    # Get all user tasks
    tasks = list(mongo.db.tasks.find({"user_id": str(user["_id"])}))
    
    # Calculate task statistics
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.get("completed", False))
    on_time_tasks = sum(1 for task in tasks if 
                      task.get("completed", False) and 
                      task.get("completed_date") and 
                      task.get("due_date") and 
                      task["completed_date"] <= task["due_date"])
    
    # Calculate cabin pressure (on-time percentage)
    cabin_pressure = round((on_time_tasks / completed_tasks * 100) if completed_tasks > 0 else 0)
    
    # Count tasks by priority
    high_priority_tasks = sum(1 for task in tasks if task.get("priority") == "high-priority")
    medium_priority_tasks = sum(1 for task in tasks if task.get("priority") == "medium-priority")
    low_priority_tasks = sum(1 for task in tasks if task.get("priority") == "low-priority")
    
    # Count overdue tasks
    current_date = datetime.now()
    overdue_tasks = sum(1 for task in tasks if 
                     not task.get("completed", False) and 
                     task.get("due_date") and 
                     task["due_date"] < current_date)
    
    # Pass all the data to the template
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
    
@app.route("/calendar")
def calendar():
    return render_template('calendar.html', active_page="calendar")

@app.route("/get_all_user_tasks")
def get_all_user_tasks():
    if 'user_id' not in session:
        return redirect('/login')

    # Get the current user from the session
    user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})

    if not user:
        session.clear()
        return redirect('/login')

    # Query the tasks for the logged-in user
    tasks = list(mongo.db.tasks.find({"user_id": get_current_user_id()}))

    # Convert ObjectId to string for JSON serialization
    for task in tasks:
        task['title'] = str(task['task'])
        task['start'] = task['due_date'].date().isoformat()

    return jsonify(tasks)

@app.route("/landing")
def landing():
    return render_template('landing-page.html')

@app.route("/contact")
def contact():
    return render_template('contact-us.html', active_page='contact')


@app.route("/todo", defaults={"filter_type": "completed"})
@app.route("/todo/<filter_type>")
def todo(filter_type):
    # Capitalize the first letter for the heading
    heading = filter_type.capitalize()
    
    # Set active_submenu for sidebar highlighting
    active_submenu = filter_type.lower()
    
    # Get the current user's tasks based on filter type
    if filter_type.lower() == "completed":
        tasks = list(mongo.db.tasks.find({"user_id": str(get_current_user_id()), "completed": True}))
    elif filter_type.lower() == "pending":
        tasks = list(mongo.db.tasks.find({"user_id": str(get_current_user_id()), "completed": False}))
    else:
        # Default to completed if invalid filter_type is provided
        tasks = list(mongo.db.tasks.find({"user_id": str(get_current_user_id()), "completed": True}))
        heading = "Completed"
        active_submenu = "completed"
    
    return render_template('todo-list.html', heading=heading, tasks=tasks, active_page='todo', active_submenu=active_submenu, filter_type=filter_type)

@app.route("/get_current_user_info")
def get_current_user_info():
    if not is_logged_in():
        return jsonify({"error": "User not logged in"}), 401 

    user = mongo.db.users.find_one({"_id": ObjectId(get_current_user_id())})

    if user:
        # Get all user tasks for statistics
        tasks = list(mongo.db.tasks.find({"user_id": str(user["_id"])}))
        
        # Calculate task statistics
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.get("completed", False))
        on_time_tasks = sum(1 for task in tasks if 
                          task.get("completed", False) and 
                          task.get("completed_date") and 
                          task.get("due_date") and 
                          task["completed_date"] <= task["due_date"])
        
        # Calculate cabin pressure (on-time percentage)
        cabin_pressure = round((on_time_tasks / completed_tasks * 100) if completed_tasks > 0 else 0)
        
        # Count tasks by priority
        high_priority_tasks = sum(1 for task in tasks if task.get("priority") == "high-priority")
        medium_priority_tasks = sum(1 for task in tasks if task.get("priority") == "medium-priority")
        low_priority_tasks = sum(1 for task in tasks if task.get("priority") == "low-priority")
        
        # Count overdue tasks
        current_date = datetime.now()
        overdue_tasks = sum(1 for task in tasks if 
                         not task.get("completed", False) and 
                         task.get("due_date") and 
                         task["due_date"] < current_date)
        
        # Add task statistics to user data
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


    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
