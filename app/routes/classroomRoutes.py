from flask import Blueprint, render_template, request, session
from app.controllers import classroomController
from app.helper.instructorHelper import accountCheck

classroom_bp = Blueprint('classroom', __name__)

@classroom_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        return classroomController.createClassroom(request.form)
    check = accountCheck()
    if check: 
        return check
    return render_template('classroomTemplate/add_classroom.html')

@classroom_bp.route('/<int:id>', methods =['GET'])
def view(id):
    check = accountCheck()
    if check: 
        return check
    return classroomController.viewClassroom(id)

@classroom_bp.route('/delete/<int:id>', methods=["GET"])
def delete(id):
    check = accountCheck()
    if check: 
        return check
    return classroomController.deleteClassroom(id)

@classroom_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        return classroomController.updateClassroom(request.form, id)
    check = accountCheck()
    if check: 
        return check
    return classroomController.getClassroom(id)