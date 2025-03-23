from flask import Flask
from flask_pymongo import PyMongo
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)  # Load configuration

# Initialize MongoDB
mongo = PyMongo(app)

# Import routes (to prevent circular imports)
from app import routes
