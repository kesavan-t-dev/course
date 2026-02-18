from flask import Flask
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from config import db
from courses.api import course_bp
from staff_availability.api import staff_avail_bp
from staffs.api import staff_bp
from course_enrollment.api import enrollment_bp
from students.api import student_bp
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    Migrate(app, db)

    app.register_blueprint(course_bp, url_prefix='/v1')
    app.register_blueprint(staff_avail_bp, url_prefix='/v1')
    app.register_blueprint(staff_bp, url_prefix='/v1')
    app.register_blueprint(enrollment_bp, url_prefix='/v1')
    app.register_blueprint(student_bp, url_prefix='/v1')
    
    @app.route('/', methods=['GET'])
    def home():
        return {
            'message': 'Course Management API',
            'version': '1.0',
            'status': 'running',
            'endpoints': {
                'COURSES': {
                    'POST /v1/courses': 'Create a new course',
                    'GET /v1/courses': 'Get all courses',
                    'PATCH /v1/courses/<course_id>': 'Update a course',
                    'DELETE /v1/courses/<course_id>': 'Delete a course'
                },
                'STAFF': {
                    'GET /v1/staff': 'Get all staff members',
                    'PATCH /v1/staff/<staff_id>': 'Update staff',
                    'PATCH /v1/staff/relieve': 'Relieve a staff member',
                    'DELETE /v1/staff/<staff_id>': 'Delete staff'
                },
                'STUDENTS': {
                    'GET /v1/students': 'Get all students',
                    'PATCH /v1/students/<student_id>': 'Update a student',
                    'DELETE /v1/students/<student_id>': 'Delete a student'
                },
                'ENROLLMENTS': {
                    'POST /v1/enrollments': 'Enroll a student in a course',
                    'GET /v1/my_courses/<student_id>': 'Get student\'s courses'
                },
                'STAFF_AVAILABILITY': {
                    'POST /v1/staff-availability': 'Add staff availability'
                }
            }
        }, 200
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
