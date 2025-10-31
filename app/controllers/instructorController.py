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
        if instructor["role"] == "admin":
            return redirect(url_for('admin.home'))
        return redirect(url_for('instructor.index'))
    else:
        flash("incorrect password", 'error')
        return redirect(url_for('instructor.login'))