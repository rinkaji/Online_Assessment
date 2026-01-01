import app as app
import MySQLdb.cursors
from flask import json, jsonify

dictFormat = MySQLdb.cursors.DictCursor

def getOptionsForQuestions(question_ids):
    cursor = app.mysql.connection.cursor(dictFormat)
    format_strings = ','.join(['%s'] * len(question_ids))
    cursor.execute(f"""
        SELECT * FROM options WHERE question_id IN ({format_strings})
    """, tuple(question_ids))
    options = cursor.fetchall()
    cursor.close()
    
    options_dict = {}
    for option in options:
        q_id = option['question_id']
        if q_id not in options_dict:
            options_dict[q_id] = []
        options_dict[q_id].append(option)
    
    return options_dict