from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_mail import Message, Mail
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from db.connection import get_db  # Use get_db for database connection
from app.utils import is_logged_in, get_current_user_id
from bson import ObjectId

auth_bp = Blueprint('auth', __name__)

# Initialize Flask-Mail (if you're using it)
mail = Mail()

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        confirm_password = request.form.get("confirm_password")
        email = request.form.get("email")

        # Validate form inputs
        if not (username and first_name and last_name and password and confirm_password and email):
            flash("All fields are required.", "error")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("auth.register"))

        db = get_db()  # Get the database connection
        existing_user = db.users.find_one({"$or": [{"username": username}, {"email": email}]})
        if existing_user:
            flash("User already exists.", "error")
            return redirect(url_for("auth.register"))

        # Hash the password
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Create user data
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

        # Insert the user into the database
        db.users.insert_one(user_data)

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()  # Get the database connection
        user = db.users.find_one({"$or": [{"username": username}, {"email": username}]})

        if user and check_password_hash(user["password"], password):
            session["user_id"] = str(user["_id"])  # Store user_id as a string
            flash("Login successful!", "success")
            return redirect(url_for("tasks.home"))

        flash("Invalid username or password", "error")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You are now logged out. See you soon!", "info")
    return redirect(url_for("main.index"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        db = get_db()  # Get the database connection
        user = db.users.find_one({"email": email})

        if user:
            reset_token = secrets.token_urlsafe(32)
            db.users.update_one({"_id": user["_id"]}, {"$set": {"reset_token": reset_token}})

            reset_url = url_for("auth.reset_password", token=reset_token, _external=True)
            msg = Message("Password Reset Request", sender="noreply@example.com", recipients=[email])
            msg.body = f"Click the link to reset your password: {reset_url}"
            mail.send(msg)

            flash("Check your email for reset instructions.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/forgot_password.html")


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    db = get_db()  # Get the database connection
    user = db.users.find_one({"reset_token": token})

    if not user:
        flash("Invalid or expired token.", "error")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        new_password = request.form.get("password")
        hashed_password = generate_password_hash(new_password)
        db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"password": hashed_password, "reset_token": None}},
        )
        flash("Password reset successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", token=token)