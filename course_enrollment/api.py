from flask import Blueprint, request
from .services import create_enrollment, get_student_courses

enrollment_bp = Blueprint('enrollment_bp', __name__)

@enrollment_bp.route('/enrollments', methods=['POST'])
def enroll_student():
    data = request.get_json(force=True)
    return create_enrollment(data)

@enrollment_bp.route('/my_courses/<string:student_id>', methods=['GET'])
def get_student_course(student_id):
    return get_student_courses(student_id)