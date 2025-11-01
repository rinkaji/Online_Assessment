from flask import redirect, session, url_for


def accountCheck():
    if not session:
        return redirect(url_for('instructor.login'))  
    elif  session and session['user']['role'] == 'instructor':
        return
    else:
        return redirect(url_for('instructor.login'))  