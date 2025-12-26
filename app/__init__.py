from flask import Flask, redirect, url_for
from app.routes.studentRoutes import student_bp 
from app.routes.instructorRoutes import instructor_bp
from app.routes.adminRoutes import admin_bp
from app.routes.classroomRoutes import classroom_bp
from app.routes.assessmentRoutes import assessment_bp
from app.routes.questionRoutes import question_bp
from app.config import Config
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    
    ##initialize the app
    app = Flask(__name__)
    
    ##initialize the database config
    app.config.from_object(Config)
    mysql.init_app(app)
    
    @app.route('/')
    def old():
        return redirect(url_for('student.login'))
    
    ##routes
    app.register_blueprint(student_bp, url_prefix = '/student')
    app.register_blueprint(instructor_bp, url_prefix = '/instructor')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(classroom_bp, url_prefix='/classroom')
    app.register_blueprint(assessment_bp, url_prefix = '/assessment')
    app.register_blueprint(question_bp, url_prefix = '/question')
    
    return app 