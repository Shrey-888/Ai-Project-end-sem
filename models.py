from app import db
from datetime import datetime

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(255))
    plot = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"<Movie {self.title}>"

class UserQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserQuery {self.id}: {self.query_text[:20]}...>"
