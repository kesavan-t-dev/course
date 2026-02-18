from staff_availability.models import db, StaffAvailability
from .models import Staff, db
from .validations import staff_schema, staffs_schema 
from staff_availability.validations import staff_avail_schema
from utils.custom_response import custom_response

def get_all_staffs():
    staff_list = Staff.query.filter_by(is_active=True).all()
    return custom_response("Staff list ", 200, staffs_schema.dump(staff_list))

def update_staffs(staff_id, data):
    try:
        staff = Staff.query.get(staff_id)
        if not staff or not staff.is_active:
            return custom_response("Staff not found", 404)

        validated_data = staff_schema.load(data, partial=True)

        for field in ['email', 'phone']:
            if field in validated_data:
                existing = Staff.query.filter(
                    getattr(Staff, field) == validated_data[field], 
                    Staff.id != staff_id
                ).first()
                if existing:
                    return custom_response(f"staff member already exists", 400)

        for key, value in validated_data.items():
            setattr(staff, key, value)

        db.session.commit()
        return custom_response("Staff updated successfully", 200, staff_schema.dump(staff))

    except Exception as e:
        db.session.rollback()
        return custom_response(str(e), 400)

def delete_staffs(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff or not staff.is_active:
        return custom_response("Staff not found", 404)

    staff.is_active = False
    db.session.commit()
    return custom_response("Staff deleted successfully", 200)

def relieve_staffs(data):
    try:
        validated_data = staff_avail_schema.load(data, partial=True)
        
        s_id = data.get('staff_id')
        req_date = validated_data.get('date')
        req_time = validated_data['start_time']
        relieve_reason = data.get('reason')

        staff = Staff.query.get(s_id)
        if not staff or not staff.is_active:
            return custom_response("Staff member not found", 404)


        availability = StaffAvailability.query.filter(
            StaffAvailability.staff_id == s_id,
            StaffAvailability.date==req_date,
            StaffAvailability.start_time==req_time,
            StaffAvailability.is_active==True
        ).first()

        if not availability:
            return custom_response("No active class found ", 404)

        availability.is_active = False 
        availability.reason = relieve_reason
        
        db.session.commit()

        return custom_response("Staff is relieved.", 200)

    except Exception as e:
        db.session.rollback()
        return custom_response(str(e), 400)



    