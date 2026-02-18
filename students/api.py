from flask import Blueprint, request
from .services import get_all_students, update_students, delete_students

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/students', methods=['GET'])
def get_student():
    return get_all_students()

@student_bp.route('/students/<string:student_id>', methods=['PATCH'])
def update_student(student_id):
    data = request.get_json(force=True)
    return update_students(student_id, data)

@student_bp.route('/students/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    return delete_students(student_id)