import random
import string
import app as app
import MySQLdb.cursors
from flask import session

dictFormat = MySQLdb.cursors.DictCursor

def getAllClassrooms(id):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("""SELECT classrooms.*, users.first_name, users.middle_name, users.last_name
                FROM classrooms
                JOIN users on classrooms.user_id = users.id
                WHERE user_id = %s""", (id,))
    data = cur.fetchall()
    cur.close()
    return data

def getClassroomCodes():
    cur = app.mysql.connection.cursor()
    cur.execute("SELECT class_code from classrooms")
    data = cur.fetchall()
    cur.close()
    return [code[0] for code in data]

def code_generator():
    codes = getClassroomCodes()
    while True:
        chars = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(chars, k=8))
        randomCode =  code[:4] + '-' + code[4:]
        if randomCode not in codes:
            return randomCode

def createClassroom(details):
    cur = app.mysql.connection.cursor()
    cur.execute("""INSERT INTO classrooms (user_id, title, class_code, description, subject)
                VALUES (%s, %s, %s, %s, %s)""", (session['user']['id'], details['title'], code_generator(), details.get('description', ''), details.get('subject', "")))
    app.mysql.connection.commit()
    cur.close()
    
def viewClassroom(id):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("""SELECT users.first_name, users.middle_name, users.last_name, classrooms.* 
                from classrooms 
                join users on users.id = classrooms.user_id 
                where classrooms.id = %s""", (id,))
    data = cur.fetchone()
    cur.close()
    return data

def deleteClassroom(id):
    cur = app.mysql.connection.cursor()
    cur.execute("DELETE FROM classrooms where id = %s", (id,))
    app.mysql.connection.commit()
    
def updateClassroom(details, id):
    cur = app.mysql.connection.cursor()
    cur.execute('''UPDATE classrooms 
                SET title = %s, description = %s
                WHERE id = %s''', 
                (details['title'],details['description'], id ))
    app.mysql.connection.commit()
    
def searchClassroom(code):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute('SELECT * from classrooms where class_code = %s' , (code,))
    data = cur.fetchone()
    cur.close()
    return data