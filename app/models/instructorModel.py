import MySQLdb.cursors
import app as app

dictFormat = MySQLdb.cursors.DictCursor

def find_account(email):
    cur = app.mysql.connection.cursor(dictFormat)
    cur.execute("SELECT * FROM users where email = %s", (email,))
    data = cur.fetchone()
    cur.close()
    return data

def insert_instructor(details):
    cur = app.mysql.connection.cursor()
    cur.execute("""INSERT INTO users (f_name, m_name, l_name, role, email, password)
                VALUES (%s,%s,%s,%s,%s,%s)""",
                (details['fname'], details['mname'], details['lname'],"instructor",details['email'],details['password'],))
    app.mysql.connection.commit()
    cur.close()
    
def getQuestions(user_id):
    cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM questions WHERE user_id = %s", (user_id,))
    data = cur.fetchall()
    cur.close()
    return data