import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine import URL

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "movie_recommender_default_key")

# Configure the PostgreSQL database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

logger.info(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import the models here
    import models
    
    # Create all tables
    db.create_all()
    
    # Initialize the movie recommender
    from movie_recommender import init_recommender
    init_recommender()
