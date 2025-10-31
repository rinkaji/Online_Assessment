import app.models.instructorModel as instructorModel
from flask import url_for, redirect, flash, render_template

def login(user):
    email = user['email']
    password = user['password']
    instructor = instructorModel.find_account(email)
    if not instructor:
        flash("account does not exists", 'error')
        return redirect(url_for('instructor.login'))
    elif instructor and password == instructor['password']:
        return render_template('instructorTemplate/instructor_class_list.html')
    else:
        flash("incorrect password", 'error')
        return redirect(url_for('instructor.login'))