from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
mongo = PyMongo()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Set configurations
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your_strong_secret_key_here")
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/task_manager")
    app.config["MAIL_SERVER"] = "smtp.example.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

    # Initialize extensions with the app
    mongo.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from app.auth.routes import auth_bp
    from app.tasks.routes import tasks_bp
    from app.profile.routes import profile_bp
    from app.main.routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(main_bp)

    return app