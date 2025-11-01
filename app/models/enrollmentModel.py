from flask import session
import app as app
import MySQLdb.cursors

dictFormat = MySQLdb.cursors.DictCursor

def addStudent(classroom):
    cur = app.mysql.connection.cursor()
    cur.execute('INSERT INTO classroom_enrollment(user_id, classroom_id) VALUES (%s, %s)', (session['user']['id'], classroom['id']))
    app.mysql.connection.commit()
    
def getClasses():
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute('''SELECT classrooms.title, users.first_name, users.middle_name, users.last_name, classrooms.description
                from classroom_enrollment
                join classrooms 
                on classroom_enrollment.classroom_id = classrooms.id
                join users
                on classroom_enrollment.user_id = users.id 
                where users.id = %s''', (session['user']['id'],))
    data = cur.fetchall()
    
    cur.close()
    return data

def searchClass(classroom_id):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute('SELECT * from classroom_enrollment where classroom_id = %s and user_id = %s', (classroom_id, session['user']['id']))
    data = cur.fetchone()
    cur.close()
    return data