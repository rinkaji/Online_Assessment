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
    cur.execute('''SELECT ce.classroom_id, c.title, c.description, u.first_name, u.middle_name, u.last_name
                from classroom_enrollment as ce
                join classrooms as c
                on ce.classroom_id = c.id
                join users as u
                on c.user_id = u.id 
                where ce.user_id = %s''', (session['user']['id'],))
    data = cur.fetchall()
    cur.close()
    return data

def searchClass(classroom_id):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute('SELECT * from classroom_enrollment where classroom_id = %s and user_id = %s', (classroom_id, session['user']['id']))
    data = cur.fetchone()
    cur.close()
    return data

def getStudents(classroomId):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute('''
                SELECT users.first_name, users.middle_name, users.last_name, users.email
                FROM classroom_enrollment
                JOIN users
                ON classroom_enrollment.user_id = users.id
                WHERE classroom_id = %s''', (classroomId,))
    data = cur.fetchall()
    cur.close()
    return data