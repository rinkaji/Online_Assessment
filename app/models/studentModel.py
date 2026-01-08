import app as app
import MySQLdb.cursors

def find_account(email):
    cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users where email = %s AND role = %s", (email,'student'))
    data = cur.fetchone()
    cur.close()
    return data

def insert_student(details):
    cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""INSERT INTO users (f_name, l_name, role, email, password)
                VALUES (%s,%s,%s,%s,%s)""",
                (details['fname'],  details['lname'],"student",details['email'],details['password'],))
    app.mysql.connection.commit()
    
    dataId = cur.lastrowid
    
    cur.execute("SELECT * FROM users where id = %s", (dataId,))
    data = cur.fetchone()
    cur.close()
    return data