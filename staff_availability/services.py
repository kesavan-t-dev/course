from config import db
from staffs.models import Staff
from .models import StaffAvailability
from .validations import staff_avail_schema
from utils.custom_response import custom_response

def staff_availability(data):
    try:
        validated_data = staff_avail_schema.load(data)    
        email = validated_data['email']
        phone = validated_data['phone']
        staff = Staff.query.filter(
            Staff.email == email
        ).first()

        if not staff:
            staff = Staff(
                name=validated_data['name'],
                email=email,
                phone=phone
            )
            db.session.add(staff)
            db.session.flush() 
        new_start = validated_data['start_time']
        new_end = validated_data['end_time']
        new_date = validated_data['date']

        conflict = StaffAvailability.query.filter(
            StaffAvailability.staff_id == staff.id,
            StaffAvailability.date == new_date,
            StaffAvailability.is_active == True,
            StaffAvailability.start_time < new_end,
            StaffAvailability.end_time > new_start
        ).first()

        if conflict:
            return custom_response(
                f"You already have a booking from {conflict.start_time} to {conflict.end_time}", 
                400
            )
        new_avail = StaffAvailability(
            staff_id=staff.id,
            course_id=validated_data['course_id'],
            date=new_date,
            start_time=new_start,
            end_time=new_end,
            reason=validated_data.get('reason'),
            is_active=True
        )
        
        db.session.add(new_avail)
        db.session.commit()
        result = staff_avail_schema.dump(new_avail)
        result['staff_id'] = staff.id 
        result['name'] = staff.name

        return custom_response("Availability recorded successfully", 201, result)

    except Exception as e:
        db.session.rollback()
        return custom_response(str(e), 400)