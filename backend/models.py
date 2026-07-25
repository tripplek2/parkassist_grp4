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

class User(db.Model):
    """Represents internal operational personnel (System Admins, Security Guards)"""
    tablename = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False) # e.g., 'Admin', 'Guard'
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoints.id', ondelete='SET NULL'), nullable=True) # Guard's duty station
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Relationships
checkpoint = db.relationship('Checkpoint', backref=db.backref('assigned_users'))
class Resident(db.Model):
    """Represents property occupants who live inside a court"""
    tablename = 'residents'

    id = db.Column(db.Integer, primary_key=True)
    court_id = db.Column(db.Integer, db.ForeignKey('courts.id', ondelete='RESTRICT'), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    unit_number = db.Column(db.String(30), nullable=False) # House or Apartment number
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Relationships
court = db.relationship('Court', backref=db.backref('residents', cascade='all, delete-orphan'))
class Visitor(db.Model):
    """Represents temporary entries requested or hosted by a resident"""
    tablename = 'visitors'

    id = db.Column(db.Integer, primary_key=True)
    host_resident_id = db.Column(db.Integer, db.ForeignKey('residents.id', ondelete='CASCADE'), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    id_number = db.Column(db.String(50), nullable=False) # National ID / Passport for checkpoint check
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Relationships
host_resident = db.relationship('Resident', backref=db.backref('hosted_visitors', cascade='all, delete-orphan'))

