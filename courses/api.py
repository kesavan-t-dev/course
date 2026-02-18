from flask import Blueprint, request
from .services import create_course, update_courses, delete_courses, get_all_course


course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    return create_course(data)

@course_bp.route('/courses', methods=['GET'])
def get_all_courses():
    return get_all_course()

@course_bp.route('/courses/<string:course_id>', methods=['PATCH'])
def update_course(course_id):
    data = request.get_json(force=True)
    return update_courses(course_id, data)

@course_bp.route('/courses/<string:course_id>', methods=['DELETE'])
def delete_course(course_id):
    return delete_courses(course_id)
