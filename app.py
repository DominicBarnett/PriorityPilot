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

@app.route('/login')
def login():
    return render_template('login-page.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv("DEBUG", "True").lower() in ("true", "1", "t"))
