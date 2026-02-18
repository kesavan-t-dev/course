from config import db
import uuid
from datetime import datetime



class StaffAvailability(db.Model):
    __tablename__ = 'staff_availability'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    staff_id = db.Column(db.String(36), db.ForeignKey('staff.id'), nullable=False)
    course_id = db.Column(db.String(36), nullable=False) 
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.Text, default=None)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    enrollment = db.relationship('Enrollment', backref='staff_availability', lazy=True)