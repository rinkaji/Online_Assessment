import app as app
import MySQLdb.cursors
from flask import json, jsonify, session


dictFormat = MySQLdb.cursors.DictCursor

def addQuestionsFromBank(question_ids, assessment_id):
    cursor = app.mysql.connection.cursor()
    for qid in question_ids:
        cursor.execute("""
            INSERT INTO question_assessment (question_id, assessment_id)
            VALUES (%s, %s)
        """, (qid, assessment_id))
    app.mysql.connection.commit()
    cursor.close()

def getQuestions(assessment_id):
    cursor = app.mysql.connection.cursor(dictFormat)
    cursor.execute("""
        SELECT 
            qa.id AS qaid, 
            q.id AS qid, q.question, q.type, q.answer, q.explanation, q.is_sensitive, q.options
        FROM question_assessment qa
        JOIN questions q 
            ON qa.question_id = q.id
        WHERE qa.assessment_id = %s
    """, (assessment_id,))
    questions = cursor.fetchall()
    cursor.close()
    return questions
