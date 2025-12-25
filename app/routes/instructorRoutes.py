from flask import Blueprint, flash, render_template, request, session, redirect, url_for
#import app.controllers.instructorController as instructorController
from app.models import classroomModel, instructorModel

instructor_bp = Blueprint('instructor', __name__)

@instructor_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('instructor.login'))

@instructor_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email',())
        password = request.form.get('password',())
        instructor = instructorModel.find_account(email)
        if not instructor:
            flash("account does not exists", 'error')
            return redirect(url_for('instructor.login'))
        elif instructor and password == instructor['password']:
            session['user'] = instructor
            if instructor["role"] == "admin":
                return redirect(url_for('admin.home'))
            return redirect(url_for('instructor.index'))
        else:
            flash("incorrect password", 'error')
            return redirect(url_for('instructor.login'))
    return render_template('/instructorTemplate/instructor_login_page.html')

@instructor_bp.route('/', methods=['GET'])
def index():
    if session and session['user']['role'] == 'instructor':
        user_id = session['user']['id']
        classrooms = classroomModel.getAllClassrooms(user_id)
        return render_template('instructorTemplate/instructor_class_list.html', classrooms = classrooms)
    flash("account does not exists", "error")
    return redirect(url_for('instructor.login'))
    