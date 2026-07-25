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

class Vehicle(db.Model):
    """Represents vehicles tracked or registered in the system"""
    tablename = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False) # e.g., Toyota
    model = db.Column(db.String(50), nullable=False) # e.g., RAV4
    color = db.Column(db.String(30), nullable=True)
    vehicle_category = db.Column(db.String(50), nullable=False) # 'Resident' or 'Visitor'
    

# Polymorphic ownership links based on your ERD
owner_resident_id = db.Column(db.Integer, db.ForeignKey('residents.id', ondelete='CASCADE'), nullable=True)
owner_visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id', ondelete='CASCADE'), nullable=True)

# Checkpoint registration tracking
registered_at_checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoints.id', ondelete='SET NULL'), nullable=True)
registered_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Relationships (Using unique backref names to prevent collisions)
owner_resident = db.relationship('Resident', backref=db.backref('vehicles', cascade='all, delete-orphan'))
owner_visitor = db.relationship('Visitor', backref=db.backref('vehicles', cascade='all, delete-orphan'))
registered_by = db.relationship('User', backref=db.backref('registered_vehicles'))

class ParkingSlot(db.Model):
    """Represents physical parking spaces assigned to specific courts"""
    tablename = 'parking_slots'

    id = db.Column(db.Integer, primary_key=True)
    court_id = db.Column(db.Integer, db.ForeignKey('courts.id', ondelete='CASCADE'), nullable=False)
    slot_number = db.Column(db.String(20), nullable=False) # e.g., 'A-101'
    status = db.Column(db.String(20), default='Available', nullable=False) # 'Available', 'Occupied', 'Reserved'
    is_visitor_slot = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Relationships
court = db.relationship('Court', backref=db.backref('parking_slots', cascade='all, delete-orphan'))

class ParkingRecord(db.Model):
    """Tracks historical and live sessions of vehicles using parking slots"""
    tablename = 'parking_records'

    id = db.Column(db.Integer, primary_key=True)
    parking_slot_id = db.Column(db.Integer, db.ForeignKey('parking_slots.id', ondelete='CASCADE'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True) # Remains NULL until vehicle exits the slot
    status = db.Column(db.String(20), default='Active', nullable=False) # 'Active', 'Completed'

# Relationships
parking_slot = db.relationship('ParkingSlot', backref=db.backref('records', cascade='all, delete-orphan'))
vehicle = db.relationship('Vehicle', backref=db.backref('parking_records', cascade='all, delete-orphan'))

class CheckpointLog(db.Model):
    """Logs every entry and exit event at a physical checkpoint"""
    tablename = 'checkpoint_logs'

    id = db.Column(db.Integer, primary_key=True)
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoints.id', ondelete='CASCADE'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True) # Guard on duty
    direction = db.Column(db.String(10), nullable=False) # 'IN' or 'OUT'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    remarks = db.Column(db.String(255), nullable=True)

# Relationships
checkpoint = db.relationship('Checkpoint', backref=db.backref('logs', cascade='all, delete-orphan'))
vehicle = db.relationship('Vehicle', backref=db.backref('logs', cascade='all, delete-orphan'))
user = db.relationship('User', backref=db.backref('logged_entries'))

class BlockingIncident(db.Model):
    """Tracks security incidents where a vehicle is blocked by another"""
    tablename = 'blocking_incidents'

    id = db.Column(db.Integer, primary_key=True)
    reporting_resident_id = db.Column(db.Integer, db.ForeignKey('residents.id', ondelete='CASCADE'), nullable=False)
    blocked_vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='Open', nullable=False) # 'Open', 'Resolved', 'Escalated'
    resolved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Relationships
reporting_resident = db.relationship('Resident', backref=db.backref('reported_incidents', cascade='all, delete-orphan'))
blocked_vehicle = db.relationship('Vehicle', backref=db.backref('blocking_incidents', cascade='all, delete-orphan'))

class Notification(db.Model):
    """System notifications dispatched to residents regarding visitors or incidents"""
    tablename = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('residents.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(30), nullable=False) # e.g., 'Incident', 'Parking', 'Visitor Access'
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Relationships
resident = db.relationship('Resident', backref=db.backref('notifications', cascade='all, delete-orphan'))

class MovementHistory(db.Model):
    """An immutable data tracking layer for deep auditing of vehicle movements"""
    tablename = 'movement_history'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False)
    checkpoint_log_id = db.Column(db.Integer, db.ForeignKey('checkpoint_logs.id', ondelete='CASCADE'), nullable=False)
    action_type = db.Column(db.String(20), nullable=False) # 'Entry', 'Exit', 'Flagged'
    archived_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Relationships
vehicle = db.relationship('Vehicle', backref=db.backref('movement_histories', cascade='all, delete-orphan'))
checkpoint_log = db.relationship('CheckpointLog', backref=db.backref('archived_movements', cascade='all, delete-orphan'))