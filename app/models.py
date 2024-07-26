from datetime import datetime
from app.exts import db


class EmailSendRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(300), nullable=False)
    tracking_id = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


class UserEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event = db.Column(db.String(100), nullable=False)
    repeated = db.Column(db.Boolean, default=False)
    platform = db.Column(db.String(30), nullable=False)
    tracking_id = db.Column(db.String(100), nullable=True, default='')
    created_at = db.Column(db.DateTime, default=datetime.now)
