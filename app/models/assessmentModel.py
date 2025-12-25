import app as app
import MySQLdb.cursors
from datetime import datetime

dictFormat = MySQLdb.cursors.DictCursor

def createAssessment(classroom_id, details):
    cur = app.mysql.connection.cursor()
    cur.execute("""INSERT INTO assessments (classroom_id, title, date, total_marks, time_limit, description, type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                (classroom_id, details['title'], datetime.now(), details.get('total_marks', ''), details.get('time_limit', ''), details.get('description', ''), details.get('type', '')))
    app.mysql.connection.commit()
    cur.close()    
    
def getAssessments(classroomId):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("""SELECT * from assessments where classroom_id = %s""", (classroomId,))
    data = cur.fetchall()
    cur.close()
    return data