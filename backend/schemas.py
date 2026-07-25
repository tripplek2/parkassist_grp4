from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from models import (
    db, Estate, Court, Checkpoint, User, Resident, 
    Visitor, Vehicle, CheckpointLog, ParkingSlot, 
    ParkingRecord, BlockingIncident, Notification, MovementHistory
)

Global schema serialization engine instance
ma = Marshmallow()

--- FOUNDATION SCHEMAS ---
class EstateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Estate
        load_instance = True
        sqla_session = db.session

class CourtSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Court
        include_fk = True
        load_instance = True
        sqla_session = db.session

class CheckpointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Checkpoint
        include_fk = True
        load_instance = True
        sqla_session = db.session

--- USER & ACTOR SCHEMAS ---
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
        sqla_session = db.session

    # Security safety: Ensures passwords can be written, but never read or leaked via API responses
    load_only = ("password_hash",)

email = fields.Email(required=True)
phone = fields.Str(required=True, validate=validate.Length(min=7, max=20))
role = fields.Str(required=True, validate=validate.OneOf(['Admin', 'Guard', 'Manager']))
class ResidentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Resident
        include_fk = True
        load_instance = True
        sqla_session = db.session

email = fields.Email(required=True)
phone = fields.Str(required=True, validate=validate.Length(min=7, max=20))
class VisitorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Visitor
        include_fk = True
        load_instance = True
        sqla_session = db.session

phone = fields.Str(required=True, validate=validate.Length(min=7, max=20))
id_number = fields.Str(required=True, validate=validate.Length(min=4, max=50))
--- ASSET & LOGISTICS SCHEMAS ---
class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        include_fk = True
        load_instance = True
        sqla_session = db.session

plate_number = fields.Str(required=True, validate=validate.Length(min=3, max=20))
vehicle_category = fields.Str(required=True, validate=validate.OneOf(['Resident', 'Visitor']))
class ParkingSlotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ParkingSlot
        include_fk = True
        load_instance = True
        sqla_session = db.session

status = fields.Str(validate=validate.OneOf(['Available', 'Occupied', 'Reserved']))
class ParkingRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ParkingRecord
        include_fk = True
        load_instance = True
        sqla_session = db.session

status = fields.Str(validate=validate.OneOf(['Active', 'Completed']))
--- LOGGING & INCIDENT SCHEMAS ---
class CheckpointLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CheckpointLog
        include_fk = True
        load_instance = True
        sqla_session = db.session

direction = fields.Str(required=True, validate=validate.OneOf(['IN', 'OUT']))
class BlockingIncidentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlockingIncident
        include_fk = True
        load_instance = True
        sqla_session = db.session

status = fields.Str(validate=validate.OneOf(['Open', 'Resolved', 'Escalated']))
class NotificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        include_fk = True
        load_instance = True
        sqla_session = db.session

class MovementHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MovementHistory
        include_fk = True
        load_instance = True
        sqla_session = db.session