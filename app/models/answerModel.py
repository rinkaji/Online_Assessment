from flask import session
import app as app
import MySQLdb.cursors


dictFormat = MySQLdb.cursors.DictCursor

def insertAnswers(uaid, answers):
    cur = app.mysql.connection.cursor()
    for answer in answers:
        cur.execute("""INSERT INTO answers (user_assessment_id, question_id, answer_text)
                    VALUES (%s, %s, %s)""", (uaid, answer['qid'], answer['answer'],))
    app.mysql.connection.commit()   
    cur.close()
    