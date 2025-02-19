from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from dotenv import load_dotenv
from flask_mail import Mail, Message  # Install via `pip install Flask-Mail`

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set configurations
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your_default_secret_key")
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/prioritypilotdev")

# Initialize MongoDB connection
mongo = PyMongo(app)

# Configure Flask-Mail for password reset emails
app.config["MAIL_SERVER"] = "smtp.example.com"  # Use a real SMTP server
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html')


# Signup Route
# Prompt user to enter First name and Last name
# Prompt user to enter password for double verification
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if not (username and password and email):
            return render_template('register.html', message='All fields are required.')

        existing_user = mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]})
        if existing_user:
            return render_template('register.html', message='User already exists.')

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        user_data = {
            'username': username,
            'password': hashed_password,
            'email': email
        }
        mongo.db.users.insert_one(user_data)

        return redirect('/login')

    return render_template('register.html')


# Login Route (Allows Login with Either Username or Email)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = mongo.db.users.find_one({'$or': [{'username': username}, {'email': username}]})

        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])  # Store as string
            return redirect('/layout')
        else:
            return render_template('login.html', message='Invalid username or password')

    return render_template('login.html')


# Layout Route
@app.route('/layout')
def layout():
    if 'user_id' not in session:
        return redirect('/login')

    user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})

    if not user:
        session.clear()
        return redirect('/login')

    return render_template('layout.html', username=user['username'])


# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# Forgot Password Route
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = mongo.db.users.find_one({'email': email})

        if user:
            reset_token = secrets.token_urlsafe(32)
            mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'reset_token': reset_token}})

            reset_url = url_for('reset_password', token=reset_token, _external=True)
            msg = Message("Password Reset Request", sender="noreply@example.com", recipients=[email])
            msg.body = f"Click the link to reset your password: {reset_url}"
            mail.send(msg)

            flash("Check your email for reset instructions.", "success")
            return redirect('/login')

    return render_template('forgot_password.html')


# Reset Password Route
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = mongo.db.users.find_one({'reset_token': token})

    if not user:
        return render_template('reset_password.html', message="Invalid or expired token.")

    if request.method == 'POST':
        new_password = request.form.get('password')
        hashed_password = generate_password_hash(new_password)
        mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'password': hashed_password, 'reset_token': None}})
        return redirect('/login')

    return render_template('reset_password.html')

@app.route("/temp-home")
def temp_home():
    return render_template('temp-home.html')
    
if __name__ == '__main__':
    app.run(debug=True)
