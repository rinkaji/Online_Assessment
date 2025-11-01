from flask import Blueprint, request, render_template, session, redirect, url_for
from app.controllers import classroomController
import app.controllers.studentController as studentController
from app.helper import studentHelper

student_bp = Blueprint('student', __name__)

@student_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('student.login'))

@student_bp.route('/login', methods=['GET', 'POST'])
def login():
    #if request.method == 'get':
    if request.method == 'POST':
        return studentController.login(request.form)
    return render_template('studentTemplate/student_login_page.html')

@student_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        return studentController.register(request.form)
    return render_template('studentTemplate/student_register_page.html')

@student_bp.route('/dashboard', methods=['GET'])
def dashboard():
    check = studentHelper.accountCheck()
    if check:
        return check
    return studentController.getClasses()

@student_bp.route('/join', methods =['GET', 'POST'])
def join():
    if request.method == "POST":
        return classroomController.joinClassroom(request.form)
    check = studentHelper.accountCheck()
    if check:
        return check
    return render_template('classroomTemplate/join_classroom.html')