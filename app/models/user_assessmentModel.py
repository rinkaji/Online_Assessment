from flask import session
import app as app
import MySQLdb.cursors


dictFormat = MySQLdb.cursors.DictCursor

def viewAssessment(assessmentId):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("""SELECT 
                a.id as aid, a.title, a.date, a.due_date, a.total_marks, a.time_limit, a.type, 
                ua.score, ua.feedback,
                u.f_name, u.l_name
                from user_assessment ua
                join assessments a 
                    on ua.assessment_id = a.id
                join classrooms c
                    on a.classroom_id = c.id
                join users u
                    on c.user_id = u.id
                where ua.user_id = %s and ua.assessment_id = %s
                """, (session['user']['id'], assessmentId))
    data = cur.fetchone()
    cur.close()
    return data

def insertAssessment(assessmentId):
    cur = app.mysql.connection.cursor()
    cur.execute("""INSERT INTO user_assessment (user_id, assessment_id)
                VALUES (%s, %s)""", (session['user']['id'], assessmentId,))
    app.mysql.connection.commit()
    cur.close()
    