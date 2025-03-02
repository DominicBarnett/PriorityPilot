from flask import Flask, render_template, request, redirect, url_for, session, flash
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


# Helper function to get the current user's ID
def get_current_user_id():
    return session.get("user_id")


# Helper function to get the current user's document
def get_current_user():
    if not is_logged_in():
        return None
    return mongo.db.users.find_one({"_id": ObjectId(get_current_user_id())})


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
            return redirect(url_for("layout"))

        flash("Invalid username or password", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/layout")
def layout():
    if not is_logged_in():
        return redirect(url_for("login"))

    user = get_current_user()
    if not user:
        session.clear()
        return redirect(url_for("login"))

    tasks = list(mongo.db.tasks.find({"user_id": get_current_user_id()}))
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


@app.route("/add-task", methods=["POST"])
def add_task():
    if not is_logged_in():
        return redirect(url_for("login"))

    task = request.form.get("task")
    priority = request.form.get("priority", "low-priority")  # Default to "low-priority"

    mongo.db.tasks.insert_one(
        {
            "user_id": get_current_user_id(),
            "task": task,
            "priority": priority,
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

    mongo.db.tasks.update_one(
        {"_id": ObjectId(task_id), "user_id": get_current_user_id()},
        {"$set": {"task": updated_task, "priority": priority}},
    )

    return "", 204  # Return an empty response with status code 204 (No Content)

@app.route("/delete-task/<task_id>", methods=["POST"])
def delete_task(task_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    mongo.db.tasks.delete_one({"_id": ObjectId(task_id), "user_id": get_current_user_id()})
    return "", 204  # Return an empty response with status code 204 (No Content)


@app.route("/toggle-completion/<task_id>", methods=["POST"])
def toggle_completion(task_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id), "user_id": get_current_user_id()})
    if task:
        completed = not task.get("completed", False)
        mongo.db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"completed": completed, "completed_date": datetime.now() if completed else None}},
        )

        # Update points and streaks
        if completed:
            user = mongo.db.users.find_one({"_id": ObjectId(get_current_user_id())})
            last_completed = user.get("last_completed", None)
            today = datetime.now()  # Use datetime.datetime instead of datetime.date

            if last_completed and (today - last_completed).days == 1:
                # Increment streak
                mongo.db.users.update_one(
                    {"_id": ObjectId(get_current_user_id())},
                    {"$inc": {"streak_days": 1}},
                )
            elif last_completed != today:
                # Reset streak
                mongo.db.users.update_one(
                    {"_id": ObjectId(get_current_user_id())},
                    {"$set": {"streak_days": 1}},
                )

            # Update last completed date
            mongo.db.users.update_one(
                {"_id": ObjectId(get_current_user_id())},
                {"$set": {"last_completed": today}},
            )

            # Award points
            mongo.db.users.update_one(
                {"_id": ObjectId(get_current_user_id())},
                {"$inc": {"points": 10}},  # Award 10 points for completing a task
            )

    return "", 204  # Return an empty response with status code 204 (No Content)


# Logout Route
@app.route("/logout")
def logout():
    print("Logout route hit")
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


@app.route("/temp-home")
def temp_home():
    return render_template('temp-home.html')

@app.route("/home")
def home():
    return render_template('home.html', active_page='home')

@app.route("/sidebar")
def sidebar():
    return render_template('sidebar.html')

@app.route("/landing")
def landing():
    return render_template('landing-page.html')

@app.route("/contact")
def contact():
    return render_template('contact-us.html', active_page='contact')
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
