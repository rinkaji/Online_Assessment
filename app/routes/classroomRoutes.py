from flask import Blueprint, flash, redirect, render_template, url_for, request, session
#from app.controllers import classroomController
from app.helper.instructorHelper import accountCheck
from app.models import assessmentModel, classroomModel, enrollmentModel, studentModel

classroom_bp = Blueprint('classroom', __name__)

@classroom_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        classroomModel.createClassroom(request.form)
        return redirect(url_for('instructor.index'))
    check = accountCheck()
    if check: 
        return check
    return render_template('classroomTemplate/add_classroom.html')

#instructor view class
@classroom_bp.route('/<int:id>', methods =['GET'])
def view(id):
    check = accountCheck()
    if check: 
        return check
    classroom = classroomModel.viewClassroom(id)
    students = enrollmentModel.getStudents(id)
    assessments = assessmentModel.getAssessments(id)
    return render_template('classroomTemplate/view_classroom.html', classroom = classroom, students = students, assessments = assessments)

#student view class
@classroom_bp.route('/view/<int:classroom_id>', methods =['GET'])
def studentView(classroom_id):
    assessments = assessmentModel.getAssessments(classroom_id)
    classroom = classroomModel.viewClassroom(classroom_id)
    students = enrollmentModel.getStudents(classroom_id)
    print("this is assessments: ", assessments)
    print("this is classroom: ", classroom)
    print("this is students: ", students)
    return render_template('studentTemplate/class_page.html', classroom = classroom, students = students, assessments = assessments)


@classroom_bp.route('/delete/<int:id>', methods=["GET"])
def delete(id):
    check = accountCheck()
    if check: 
        return check
    classroomModel.deleteClassroom(id)
    flash("successfully deleted", "message")
    return redirect(url_for('instructor.index'))

@classroom_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        classroomModel.updateClassroom(request.form, id)
        return redirect(url_for('instructor.index'))
    check = accountCheck()
    if check: 
        return check
    classroom = classroomModel.viewClassroom(id)
    return render_template('classroomTemplate/edit_classroom.html', classroom = classroom)

