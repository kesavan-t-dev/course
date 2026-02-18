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
    
    return app

# Create app instance for Vercel
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
