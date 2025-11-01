from flask import Blueprint, request, render_template, session, redirect, url_for
import app.controllers.studentController as studentController

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
    if not session:
        return redirect(url_for('student.login'))
    return studentController.getClasses()