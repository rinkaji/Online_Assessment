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
