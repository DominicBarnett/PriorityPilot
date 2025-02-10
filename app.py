from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if available
load_dotenv()

app = Flask(__name__)

# Set configurations directly in app.config
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your_default_secret_key")
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/prioritypilotdev")

# Initialize MongoDB connection
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

# Signup/Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Validate form data
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if not (username and password and email):
            return render_template('register.html', message='All feilds are required.')
        
        # Check if user already exists
        existing_user = mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]})
        if existing_user:
            return render_template('register.html', message='User already exists.')
        
        # Block the Password
        hashed_password = generate_password_hash(password)

        # Insert user data into the database
        user_data ={
            'username': username,
            'password': hashed_password,
            'email': email
        }
        mongo.db.users.insert_one(user_data)

        return redirect('/login')
    
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Retrieve user data from the database
        user = mongo.db.users.find_one({'username': username})

        # Check if username exists and password is correct
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/layout')
        else:
            return render_template('login.html', message='Invalid username or password')
        
    return render_template('login.html')

# Layout Route
@app.route('/layout')
def layout():
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session['user_id']
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})

    if not user:
        session.clear()
        return redirect('/login')
    
    return render_template('layout.html', username=user['username'])

@app.route('/logout')
def logout():
    # Clear Session
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv("DEBUG", "True").lower() in ("true", "1", "t"))
