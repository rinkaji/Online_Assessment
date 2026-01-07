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
    
def getAnswers(uaid):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("""SELECT 
                q.question, q.answer, q.type, q.options, 
                a.answer_text, a.explanation
                FROM answers a
                JOIN questions q
                    ON a.question_id = q.id 
                WHERE a.user_assessment_id = %s""", (uaid,))
    data = cur.fetchall()
    cur.close()
    return data
    
def getAnswersByUaids(uaids):
    cur = app.mysql.connection.cursor(dictFormat)
    studentAnswers = []
    for uaid in uaids:
        cur.execute("""select 
                    a.*, q.* 
                    from answers a
                    join questions q 
                        on a.question_id = q.id
                    where user_assessment_id = %s""" , (uaid,))
        studentAnswers.append(cur.fetchall())
    cur.close()
    return studentAnswers

def updateAnswers(data):
    answerIds = data['answerIDs']
    explanation = data['explanations']
    cur = app.mysql.connection.cursor()
    for index, answerId in enumerate(answerIds):
        cur.execute("""update answers 
                    set explanation = %s
                    where id = %s""" ,(explanation[index], answerId))
    app.mysql.connection.commit()
    cur.close
   