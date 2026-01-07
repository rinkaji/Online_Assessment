import app as app
import MySQLdb.cursors
from datetime import datetime

dictFormat = MySQLdb.cursors.DictCursor

def createAssessment(classroom_id, details):
    cur = app.mysql.connection.cursor()
    cur.execute("""INSERT INTO assessments (classroom_id, title, date, total_marks, time_limit, description, type, due_date, is_automatic)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                (classroom_id, details['title'], datetime.now(), details.get('total_marks', ''), details.get('time_limit', ''), details.get('description', ''), details.get('type', ''), details.get('due_date', ''), details.get('is_automatic', '')))
    # print(datetime.now())
    app.mysql.connection.commit()
    cur.close()    
    
def getAssessments(classroomId, status = ""):
    cur = app.mysql.connection.cursor(dictFormat)
    if status:
        cur.execute("""SELECT * from assessments where classroom_id = %s and status = %s""", (classroomId, status))
    else:
        cur.execute("""SELECT * from assessments where classroom_id = %s""", (classroomId,))
    data = cur.fetchall()
    cur.close()
    return data

def viewAssessment(assessmentId):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("""SELECT * from assessments where id = %s""", (assessmentId,))
    data = cur.fetchone()
    cur.close()
    return data

def isAutomatic(assessmentId):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("""SELECT id, is_automatic from assessments where id = %s""", (assessmentId,))
    data = cur.fetchone()
    cur.close()
    data['is_automatic'] = True if data['is_automatic'] == 1 else False
    return data

def updateQuestionCount(assessmentId, questionCount):
    cur = app.mysql.connection.cursor()
    cur.execute("""UPDATE assessments SET total_marks = %s WHERE id = %s""", (questionCount, assessmentId))
    app.mysql.connection.commit()
    cur.close()

def deployAssessment(assessmentId):
    cur = app.mysql.connection.cursor()
    cur.execute("""UPDATE assessments SET status = 'deployed' WHERE id = %s""", (assessmentId,))
    app.mysql.connection.commit()
    cur.close()
