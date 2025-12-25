from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from app.models import adminModel, instructorModel, studentModel


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET'])
def home():
    if not session:
        return redirect(url_for('instructor.login'))
    return render_template('adminTemplate/admin_homepage.html')

##students side
@admin_bp.route('/student', methods=["GET"])
def getStudents():
    if not session:
        return redirect(url_for('instructor.login'))
    students = adminModel.getAllUsers('student')
    return render_template('adminTemplate/admin_students_list.html', students = students)

@admin_bp.route('/student/register', methods=["GET", 'POST'])
def addStudent():
    if not session:
        return redirect(url_for('instructor.login'))
    if request.method == "POST":
        student = studentModel.find_account(request.form.get('email',''))
        if student:
            flash("account already exists", 'error')
            return redirect(url_for('admin.addStudent'))
        studentModel.insert_student(request.form)
        return redirect(url_for('admin.getStudents'))
    return render_template('adminTemplate/admin_student_registration.html')

@admin_bp.route('/student/delete/<int:id>', methods= ['GET'])
def removeStudent(id):
    if not session:
        return redirect(url_for('instructor.login'))
    adminModel.deleteUser(id)
    return redirect(url_for('admin.getStudents'))


##instructors side
@admin_bp.route('/instructor', methods=["GET"])
def getInstructors():
    if not session:
        return redirect(url_for('instructor.login'))
    instructors = adminModel.getAllUsers('instructor')
    return render_template('adminTemplate/admin_instructors_list.html', instructors = instructors)

@admin_bp.route('/instructor/register', methods=["GET", 'POST'])
def addInstructor():
    if not session:
        return redirect(url_for('instructor.login'))
    if request.method == "POST":
        #return adminController.insertInstructor(request.form)
        instructor = instructorModel.find_account(request.form.get('email',''))
        if instructor:
            flash("account already exists", 'error')
            return redirect(url_for('admin.addInstructor'))
        instructorModel.insert_instructor(request.form)
        return redirect(url_for('admin.getInstructors'))
    return render_template('adminTemplate/admin_instructor_registration.html')

@admin_bp.route('/instructor/delete/<int:id>', methods= ['GET'])
def removeInstructor(id):
    if not session:
        return redirect(url_for('instructor.login'))
    adminModel.deleteUser(id)
    return redirect(url_for('admin.getInstructors'))
 