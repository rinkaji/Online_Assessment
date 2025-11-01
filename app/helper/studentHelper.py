from flask import redirect, session, url_for


def accountCheck():
    if not session:
        return redirect(url_for('student.login'))  
    elif  session and session['user']['role'] == 'student':
        return
    else:
        return redirect(url_for('student.login'))  