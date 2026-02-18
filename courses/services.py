from .models import Course
from config import db
from .validations import course_schema
from utils.custom_response import custom_response
from datetime import date
from .validations import CourseSchema

def get_all_course():
    course_list = Course.query.filter_by(is_active=True).all()
    result = CourseSchema(many=True).dump(course_list)
    return custom_response("Course list", 200, result)

def create_course(data):
    try:
        validated_data = course_schema.load(data)
        name = validated_data['c_name']
        new_date = validated_data['date']
        new_start = validated_data['start_time']
        new_end = validated_data['end_time']

        if new_date < date.today():
            return custom_response(
                "Past date is not allowed",
                400
            )
        
        conflict = Course.query.filter(
            Course.c_name == name,
            Course.date == new_date,
            Course.start_time < new_end,
            Course.end_time > new_start
        ).first()
        
        if conflict:
            return custom_response(
                message=f"The {name}course is already scheduled on that {new_start} to {new_end}",
                status_code=400
            )

        new_course = Course(c_name=validated_data['c_name'],
                                desc=validated_data['desc'],
                                date=validated_data['date'],
                                start_time=validated_data['start_time'],
                                end_time=validated_data['end_time'],
                            )
        db.session.add(new_course)
        db.session.commit()
        return custom_response("Course created successfully", 201, course_schema.dump(new_course))
        
    except Exception as e:
        db.session.rollback()
        return custom_response(f"Validation Error: {str(e)}", 400)


def update_courses(course_id, data):
    try:
        validated_data = course_schema.load(data, partial=True)
        course = Course.query.get(course_id)
        new_date = validated_data.get('date', course.date)
        new_start = validated_data.get('start_time', course.start_time)
        new_end = validated_data.get('end_time', course.end_time)
        if not course:
            return custom_response("Course not found", 404)


        if any(key in validated_data for key in ['date', 'start_time', 'end_time']):
            conflict = Course.query.filter(
                Course.id != course_id,  
                Course.c_name == course.c_name,
                Course.date == new_date,
                Course.start_time < new_end,
                Course.end_time > new_start
            ).first()
            
            if conflict:
                return custom_response("Update failed: Time overlap", 400)

        for key, value in validated_data.items():
            setattr(course, key, value)
            
        if new_date < date.today():
            return custom_response(
                "Past date is not allowed",
                400
            )
        db.session.commit()
        return custom_response("Course updated successfully", 200, course_schema.dump(course))

    except Exception as e:
        db.session.rollback()
        return custom_response(str(e), 400)


def delete_courses(course_id):
    course = Course.query.get(course_id)
    if not course:
        return custom_response("Course not found", 404)
    
    course.is_active = False 
    db.session.commit()
    
    return custom_response("Course deleted successfully", 200)
