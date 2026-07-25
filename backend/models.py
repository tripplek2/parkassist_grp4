from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

#Global database instance
db = SQLAlchemy()

class Estate(db.Model):
    tablename = 'estates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Court(db.Model):
    tablename = 'courts'

    id = db.Column(db.Integer, primary_key=True)
    estate_id = db.Column(db.Integer, db.ForeignKey('estates.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Relationships
estate = db.relationship('Estate', backref=db.backref('courts', cascade='all, delete-orphan'))
class Checkpoint(db.Model):
    tablename = 'checkpoints'

    id = db.Column(db.Integer, primary_key=True)
    estate_id = db.Column(db.Integer, db.ForeignKey('estates.id', ondelete='CASCADE'), nullable=False)
    court_id = db.Column(db.Integer, db.ForeignKey('courts.id', ondelete='SET NULL'), nullable=True) # Optional link to specific court
    name = db.Column(db.String(100), nullable=False) # e.g., 'Main Gate East'
    type = db.Column(db.String(50), nullable=False)  # e.g., 'Vehicle', 'Pedestrian'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Relationships
estate = db.relationship('Estate', backref=db.backref('checkpoints', cascade='all, delete-orphan'))
court = db.relationship('Court', backref=db.backref('checkpoints'))
