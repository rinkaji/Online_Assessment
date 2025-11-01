from flask import Blueprint, flash, render_template, request, session, redirect, url_for
import app.controllers.instructorController as instructorController

instructor_bp = Blueprint('instructor', __name__)

@instructor_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('instructor.login'))

@instructor_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        return instructorController.login(request.form)
    return render_template('/instructorTemplate/instructor_login_page.html')

@instructor_bp.route('/', methods=['GET'])
def index():
    if session and session['user']['role'] == 'instructor':
        return instructorController.getClassrooms()
    flash("account does not exists", "error")
    return redirect(url_for('instructor.login'))
    