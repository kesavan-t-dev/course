from config import db
import uuid

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    availabilities = db.relationship('StaffAvailability', backref='staff', lazy=True)