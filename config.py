class Config:
    """Configuration settings for Flask and MongoDB."""

    DEBUG = True  # Enable debug mode
    SECRET_KEY = "your_secret_key_here"  # Change this to a strong random key
    MONGO_URI = "mongodb://localhost:27017/signify_db"  # MongoDB Compass connection
