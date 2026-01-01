import app as app
import MySQLdb.cursors
from flask import json, jsonify, session


dictFormat = MySQLdb.cursors.DictCursor

def createQuestion(data, user_id):
    question_text = data.get('question')
    question_type = data.get('type')
    correct_answer = data.get('answer', '')
    explanation = data.get('explanation', '')
    assessment_id = data.get('assessment_id', '')
    ql = data.get('ql', 0)
    is_sensitive = data.get('is_sensitive', '')
    options = data.get('options', '')
    if options:
        options = ','.join(options)
    
    cursor = app.mysql.connection.cursor()
    # include is_sensitive when saving identification questions
    cursor.execute("""
        INSERT INTO questions (user_id, question, type, answer, explanation, is_sensitive, options)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user_id, question_text, question_type, correct_answer, explanation, is_sensitive, options))

    question_id = cursor.lastrowid

    # insert mapping into question_assessment
    if ql <= 0:
        cursor.execute("""
            INSERT INTO question_assessment (question_id, assessment_id)
            VALUES (%s, %s)
        """, (question_id, assessment_id))
    
    app.mysql.connection.commit()
    cursor.close()
    return question_id

def getQuestions(assessmentId):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("""
        SELECT q.id AS qid, q.user_id, q.question, q.type, q.answer, q.explanation, q.is_sensitive, q.options
        FROM question_assessment aq
        JOIN questions q ON q.id = aq.question_id
        WHERE aq.assessment_id = %s
        ORDER BY q.id
    """, (assessmentId,))
    rows = cur.fetchall()
    cur.close()

    # group options under each question
    questions = []
    lookup = {}
    for row in rows:
        qid = row['qid']
        if qid not in lookup:
            q = {
                'id': qid,
                'user_id': row.get('user_id'),
                'question': row.get('question'),
                'type': row.get('type'),
                'answer': row.get('answer'),
                'explanation': row.get('explanation'),
                # normalize is_sensitive to boolean (handles 0/1, '0'/'1', True/False)
                'is_sensitive': int(row.get('is_sensitive')) if row.get('is_sensitive') is not None else False,
                'options': row.get('options').split(',') if row.get('options') else []
            }
            lookup[qid] = q
            questions.append(q)
    return questions

def getAllQuestions():
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("""
        select * from questions 
        where user_id  = %s
    """, (session['user']['id'],))
    rows = cur.fetchall()
    cur.close()

    questions = []
    for row in rows:
        q = {
            'id': row['id'],
            'user_id': row.get('user_id'),
            'question': row.get('question'),
            'type': row.get('type'),
            'answer': row.get('answer'),
            'explanation': row.get('explanation'),
            # normalize is_sensitive to boolean (handles 0/1, '0'/'1', True/False)
            'is_sensitive': int(row.get('is_sensitive')) if row.get('is_sensitive') is not None else False,
            'options': row.get('options').split(',') if row.get('options') else []
        }
        questions.append(q)
    return questions

def deleteQuestion(questionId, assessmentId=None):
    cur = app.mysql.connection.cursor()
    if assessmentId is not None:
        cur.execute("DELETE FROM question_assessment WHERE question_id = %s AND assessment_id = %s", (questionId, assessmentId))
    else:
        cur.execute("DELETE FROM questions WHERE id = %s", (questionId,))
    app.mysql.connection.commit()
    cur.close()
    
def viewQuestion(questionId):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("SELECT * FROM questions WHERE id = %s", (questionId,))
    data = cur.fetchone()
    cur.close()
    return data   

def updateQuestion(questionId, data):
    question_text = data.get('question')
    question_type = data.get('type')
    correct_answer = data.get('answer', '')
    explanation = data.get('explanation', '')
    is_sensitive = bool(data.get('is_sensitive', False))
    options = data.get('options', '')
    options = ','.join(options) if options else ''
    cursor = app.mysql.connection.cursor()
    cursor.execute("""
        UPDATE questions
        SET question = %s,
            `type` = %s,
            answer = %s,
            explanation = %s,
            is_sensitive = %s,
            options = %s
        WHERE id = %s
    """, (question_text, question_type, correct_answer, explanation, is_sensitive, options, questionId))
    
    app.mysql.connection.commit()
    cursor.close()


