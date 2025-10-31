import app.models.adminModel as adminModel
import app.models.studentModel as studentModel
import app.models.instructorModel as instructorModel
from flask import render_template, flash, url_for, redirect

def getStudents():
    students = adminModel.getAllUsers('student')
    return render_template('adminTemplate/admin_students_list.html', students = students)

def insertStudent(user):
    student = studentModel.find_account(user['email'])
    if student:
        flash("account already exists", 'error')
        return redirect(url_for('admin.addStudent'))
    studentModel.insert_student(user)
    return redirect(url_for('admin.getStudents'))

def getInstructors():
    instructors = adminModel.getAllUsers('instructor')
    return render_template('adminTemplate/admin_instructors_list.html', instructors = instructors)

def insertInstructor(user):
    instructor = instructorModel.find_account(user['email'])
    if instructor:
        flash("account already exists", 'error')
        return redirect(url_for('admin.addInstructor'))
    instructorModel.insert_instructor(user)
    return redirect(url_for('admin.getInstructors'))

def deleteUser(id, user):
    adminModel.deleteUser(id)
    if user == 'instructor':
        return redirect(url_for('admin.getInstructors'))
    else:
        return redirect(url_for('admin.getStudents'))
    