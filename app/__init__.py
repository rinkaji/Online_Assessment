from flask import Flask
from app.routes.studentRoutes import student_bp 
from app.routes.instructorRoutes import instructor_bp
from app.config import Config
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    
    ##initialize the app
    app = Flask(__name__)
    
    ##initialize the database config
    app.config.from_object(Config)
    mysql.init_app(app)
    
    ##routes
    app.register_blueprint(student_bp, url_prefix = '/student')
    app.register_blueprint(instructor_bp, url_prefix = '/instructor')
    
    
    return app 