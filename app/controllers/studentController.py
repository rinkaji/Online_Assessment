import app.models.studentModel as studentModel
from flask import render_template, flash, url_for, redirect

def login(user):
    email = user['email']
    password = user['password']
    data = studentModel.find_account(email)
    if not data:
        flash('account does not exists', 'error')
        return redirect(url_for('student.login'))
    elif password == data['password']:
        print("successfully")
        return render_template('studentTemplate/show_classes_page.html')
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
    return render_template('studentTemplate/show_classes_page.html')
    
    