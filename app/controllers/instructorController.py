from app.models import classroomModel, instructorModel
from flask import url_for, redirect, flash, render_template, session

def login(user):
    email = user['email']
    password = user['password']
    instructor = instructorModel.find_account(email)
    if not instructor:
        flash("account does not exists", 'error')
        return redirect(url_for('instructor.login'))
    elif instructor and password == instructor['password']:
        session['user'] = instructor
        if instructor["role"] == "admin":
            return redirect(url_for('admin.home'))
        return redirect(url_for('instructor.index'))
    else:
        flash("incorrect password", 'error')
        return redirect(url_for('instructor.login'))
    
def getClassrooms():
    user_id = session['user']['id']
    classrooms = classroomModel.getAllClassrooms(user_id)
    return render_template('instructorTemplate/instructor_class_list.html', classrooms = classrooms)