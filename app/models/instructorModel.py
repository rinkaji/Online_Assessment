import MySQLdb.cursors
import app as app

def find_account(email):
    cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users where email = %s AND role = %s", (email,'instructor'))
    data = cur.fetchone()
    cur.close()
    return data

def insert_instructor(details):
    cur = app.mysql.connection.cursor()
    cur.execute("""INSERT INTO users (first_name, middle_name, last_name, role, email, password)
                VALUES (%s,%s,%s,%s,%s,%s)""",
                (details['fname'], details['mname'], details['lname'],"instructor",details['email'],details['password'],))
    app.mysql.connection.commit()
    cur.close()