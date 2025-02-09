from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile('config.py')
# mongo = PyMongo(app)

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
        
        # Block the Password
        hashed_password = generate_password_hash(password)

        # Database Code Goes Here

        return redirect('/login')
    
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Retrieve user data from the database
        # Database query code goes here

        # Check if username exists and password is correct
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/layout')
        else:
            return render_template('login.html', message='Invalid username or password')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear Session
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)