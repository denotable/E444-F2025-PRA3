# project/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = "post"
    id    = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text  = db.Column(db.Text, nullable=False)

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return f"<title {self.title}>"
