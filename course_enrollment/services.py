from config import db
from .models import Enrollment
from students.models import Student
from courses.models import Course
from .validations import enrollment_schema, enrollments_schema
from utils.custom_response import custom_response
from staff_availability.models import StaffAvailability
from datetime import date

def create_enrollment(data):
    try:
        validated_data = enrollment_schema.load(data)
        
        c_id = validated_data['course_id']
        req_date = validated_data['date']
        s_time = validated_data['start_time']
        e_time = validated_data['end_time']

        if req_date < date.today():
            return custom_response("Past date is not allowed", 400)

        availability = StaffAvailability.query.filter(
            StaffAvailability.course_id == c_id,
            StaffAvailability.date == req_date, 
            StaffAvailability.start_time <= s_time, 
            StaffAvailability.end_time >= e_time,   
            StaffAvailability.is_active == True
        ).first()

        if not availability:
            return custom_response(
                "No staff is available.", 
                404
            )

        student = Student.query.filter_by(phone=validated_data['phone']).first()
        if not student:
            student = Student(
                name=validated_data['name'],
                phone=validated_data['phone'],
                email=validated_data['email'],
                gender=validated_data.get('gender'),
                age=validated_data.get('age')
            )
            db.session.add(student)


        duplicate = Enrollment.query.filter_by(
            student_id=student.id,
            staff_avail_id=availability.id,
            is_active=True
        ).first()

        if duplicate:
            return custom_response("You already enrolled.", 400)

        new_enrollment = Enrollment(
            student_id=student.id,
            staff_avail_id=availability.id, 
            course_id=c_id,
            date=req_date,
            start_time=s_time,
            end_time=e_time
        )
        
        db.session.add(new_enrollment)
        db.session.commit()
        
        return custom_response("Enrollment successful", 201, enrollment_schema.dump(new_enrollment))

    except Exception as e:
        db.session.rollback()
        return custom_response(str(e), 400)
    
def get_student_courses(student_id):
    try:
        query = db.session.query(
            Enrollment.id,
            Student.name.label('name'),
            Course.c_name.label('course_name'),
            Enrollment.date,
            Enrollment.start_time,
            Enrollment.end_time,
        ).join(Student, Enrollment.student_id == Student.id
        ).join(Course, Enrollment.course_id == Course.id
        ).filter(
             Enrollment.student_id == student_id, 
             Enrollment.is_active == True
         ).all()

        if not query:
            return custom_response("No active enrollments found", 404, [])

        result = enrollments_schema.dump(query)
        
        return custom_response("My Course List !", 200, result)

    except Exception as e:
        return custom_response(str(e), 400)
