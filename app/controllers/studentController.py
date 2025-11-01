import app.models.studentModel as studentModel
from flask import render_template, flash, url_for, redirect, session

def login(user):
    email = user['email']
    password = user['password']
    data = studentModel.find_account(email)
    if not data:
        flash('account does not exists', 'error')
        return redirect(url_for('student.login'))
    elif password == data['password']:
        session['user'] = data
        print("successfully")
        return redirect(url_for('student.dashboard'))
    else:
        flash('incorrect password', 'error')
        return redirect(url_for('student.login'))
    
def register(details):
    email = details['email']
    data = studentModel.find_account(email)
    if data:
        flash("account already exists", 'error')
        return redirect(url_for('student.register'))
    studentModel.insert_student(details)
    session['user'] = data
    return redirect(url_for('student.dashboard'))

def getClasses():
    return render_template('studentTemplate/student_show_classes_page.html')