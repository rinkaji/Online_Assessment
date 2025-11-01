from flask import flash, redirect, render_template, url_for
from app.models import classroomModel, enrollmentModel


def createClassroom(details):
    classroomModel.createClassroom(details)
    return redirect(url_for('instructor.index'))

def viewClassroom(id):
    classroom = classroomModel.viewClassroom(id)
    return render_template('classroomTemplate/view_classroom.html', classroom = classroom)

def deleteClassroom(id):
    classroomModel.deleteClassroom(id)
    flash("successfully deleted", "message")
    return redirect(url_for('instructor.index'))

def getClassroom(id):
    classroom = classroomModel.viewClassroom(id)
    return render_template('classroomTemplate/edit_classroom.html', classroom = classroom)

def updateClassroom(details, id):
    classroomModel.updateClassroom(details, id)
    return redirect(url_for('instructor.index'))

def joinClassroom(code):
    classRoom = classroomModel.searchClassroom(code['code'])
    
    if not classRoom:
        flash("classroom does not exists", 'error') 
        return redirect(url_for('student.dashboard'))
    
    exists = enrollmentModel.searchClass(classRoom['id'])
    if exists:
        flash("classroom already joined", 'error') 
        return redirect(url_for('student.dashboard'))
    
    enrollmentModel.addStudent(classRoom)
    return redirect(url_for('student.dashboard'))