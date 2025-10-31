from flask import Blueprint, render_template, request
import app.controllers.instructorController as instructorController

instructor_bp = Blueprint('instructor', __name__)

@instructor_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        return instructorController.login(request.form)
    return render_template('/instructorTemplate/instructor_login_page.html')