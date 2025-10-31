from flask import Blueprint, render_template, request
import app.controllers.adminController as adminController


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET'])
def home():
    return render_template('adminTemplate/admin_homepage.html')

##students side
@admin_bp.route('/student', methods=["GET"])
def getStudents():
    return adminController.getStudents()
@admin_bp.route('/student/register', methods=["GET", 'POST'])
def addStudent():
    if request.method == "POST":
        return adminController.insertStudent(request.form)
    return render_template('adminTemplate/admin_student_registration.html')
@admin_bp.route('/student/delete/<int:id>', methods= ['GET'])
def removeStudent(id):
    return adminController.deleteUser(id, 'student')


##instructors side
@admin_bp.route('/instructor', methods=["GET"])
def getInstructors():
    return adminController.getInstructors()

@admin_bp.route('/instructor/register', methods=["GET", 'POST'])
def addInstructor():
    if request.method == "POST":
        return adminController.insertInstructor(request.form)
    return render_template('adminTemplate/admin_instructor_registration.html')

@admin_bp.route('/instructor/delete/<int:id>', methods= ['GET'])
def removeInstructor(id):
    return adminController.deleteUser(id, 'instructor')