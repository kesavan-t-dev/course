from config import db
from .models import Student
from .validations import student_schema, students_schema
from utils.custom_response import custom_response

def get_all_students():
    students = Student.query.filter_by(is_active=True).all()
    return custom_response("Students List !", 200, students_schema.dump(students))

def update_students(student_id, data):
    try:
        student = Student.query.get(student_id)
        if not student or not student.is_active:
            return custom_response("Student not found", 404)
        validated_data = student_schema.load(data, partial=True)
        for key, value in validated_data.items():
            setattr(student, key, value)
        db.session.commit()
        return custom_response("Student profile updated", 200, student_schema.dump(student))
    except Exception as e:
        db.session.rollback()
        return custom_response(str(e), 400)

def delete_students(student_id):
    student = Student.query.get(student_id)
    if not student or not student.is_active:
        return custom_response("Student not found", 404)
    student.is_active = False
    db.session.commit()
    return custom_response("Student deleted successfully", 200)