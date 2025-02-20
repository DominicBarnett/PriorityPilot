from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
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


@app.route('/')
def index():
    return render_template('index.html')


# Signup Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')

        if not (username and first_name and last_name and password and confirm_password and email):
            return render_template('register.html', message='All fields are required.')

        if password != confirm_password:  # Check if passwords match
            return render_template('register.html', message='Passwords do not match.')

        existing_user = mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]})
        if existing_user:
            return render_template('register.html', message='User already exists.')

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")


        user_data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
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

    user_id = ObjectId(session['user_id'])

    #Fetch user's task, notes, and todos
    tasks = list(mongo.db.tasks.find({'user_id': user_id}))
    notes = list(mongo.db.notes.find({'user_id': user_id}))
    todos = list(mongo.db.todos.find({'user_id': user_id}))

    return render_template('temp-home.html', tasks=tasks, notes=notes, todos=todos)

@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = ObjectId(session['user_id'])
    content = request.form.get('content')
    data_type = request.form.get('data_type')

    if data_type == 'task':
        mongo.db.tasks.insert_one({'user_id': user_id, 'content': content})
    elif data_type == 'note':
        mongo.db.notes.insert_one({'user_id': user_id, 'content': content})
    elif data_type == 'todo':
        mongo.db.todos.insert_one({'user_id': user_id, 'content': content})
    
    return redirect(url_for('layout'))

# Update Data (tasks, Notes, Todos)
@app.route('/update/<data_type>/<data_id>', methods=['POST'])
def update(data_type, data_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    updated_content = request.form.get('content')

    if data_type == 'task':
        mongo.db.tasks.update_one({'_id': ObjectId(data_id)}, {'$set': {'content': updated_content}})
    elif data_type == 'note':
        mongo.db.notes.update_one({'_id': ObjectId(data_id)}, {'$set': {'content': updated_content}})
    elif data_type == 'todo':
        mongo.db.todos.update_one({'_id': ObjectId(data_id)}, {'$set': {'content': updated_content}})

    return redirect(url_for('layout'))

@app.route('/delete/<data_type>/<data_id>', methods=['POST'])
def delete(data_type, data_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    if data_type == 'task':
        mongo.db.tasks.delete_one({'_id': ObjectId(data_id)})
    elif data_type == 'note':
        mongo.db.notes.delete_one({'_id': ObjectId(data_id)})
    elif data_type == 'todo':
        mongo.db.todos.delete_one({'_id': ObjectId(data_id)})

    return redirect(url_for('layout'))

# Logout Route
@app.route('/logout')
def logout():
    print("Logout route hit")
    session.clear()
    flash("You are now logged out. See you soon!", "info")
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

@app.route("/home")
def home():
    return render_template('home.html', active_page='home')

@app.route("/sidebar")
def sidebar():
    return render_template('sidebar.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')
    
@app.route("/calendar")
def calendar():
    return render_template('calendar.html')

@app.route("/get_all_user_tasks")
def get_all_user_tasks():
    tasks = [
        {"title": "Task 1", "start": "2025-02-26"},
        {"title": "Task 3", "start": "2025-02-26"},
        {"title": "Task 2", "start": "2025-02-27"}
    ]
    return jsonify(tasks)
@app.route("/landing")
def landing():
    return render_template('landing-page.html')

@app.route("/contact")
def contact():
    return render_template('contact-us.html', active_page='contact')
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

