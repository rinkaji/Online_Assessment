from flask import session
import app as app
import MySQLdb.cursors


dictFormat = MySQLdb.cursors.DictCursor

def viewAssessment(assessmentId):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("""SELECT 
                a.id as aid, a.title, a.date, a.due_date, a.total_marks, a.time_limit, a.type, 
                ua.score, ua.feedback, ua.id as uaid,
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
 
def getUaidByAid(aid):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("""SELECT id FROM user_assessment
                WHERE user_id = %s AND assessment_id = %s""", (session['user']['id'], aid,))
    data = cur.fetchone()
    cur.close()
    return data['id']

def updateAssessment(uaid, score = 0):
    cur = app.mysql.connection.cursor()
    if not score:
        cur.execute("""UPDATE user_assessment
                    SET is_finished = %s, submitted_at = NOW()
                    WHERE id = %s""", ("submitted", uaid,))
    else:
        cur.execute("""UPDATE user_assessment
                    SET is_finished = %s, score = %s, submitted_at = NOW()
                    WHERE id = %s""", ("checked", score, uaid))
    app.mysql.connection.commit()
    cur.close()
    
def isAssessementFinished(aid):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("""SELECT is_finished FROM user_assessment
                WHERE user_id = %s AND assessment_id = %s""",  (session['user']['id'], aid))
    data = cur.fetchone()
    cur.close()
    return data['is_finished']

def getStudentsWithAssessment(assessment_id):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute('''
                SELECT users.f_name, users.l_name, ua.score, ua.is_finished, ua.id AS uaid
                FROM user_assessment AS ua
                JOIN users
                ON ua.user_id = users.id
                WHERE ua.assessment_id = %s''', (assessment_id,))
    data = cur.fetchall()
    cur.close()
    return data

def updateUserAssessment(uaid, details):
    cur = app.mysql.connection.cursor()
    cur.execute("""
                update user_assessment
                set is_finished = %s, score = %s, feedback = %s
                where id = %s""", ("checked", details['score'], details['comment'], uaid))
    app.mysql.connection.commit()
    cur.close

def getUserAssessment(uaid):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("select * from user_assessment where id = %s", (uaid, ))
    data = cur.fetchone()
    cur.close
    return data