import app as app
import MySQLdb.cursors

def find_account(email):
    cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users where email = %s AND role = %s", (email,'student'))
    data = cur.fetchone()
    cur.close()
    return data

def insert_student(details):
    cur = app.mysql.connection.cursor()
    cur.execute("""INSERT INTO users (first_name, middle_name, last_name, role, email, password)
                VALUES (%s,%s,%s,%s,%s,%s)""",
                (details['fname'], details['mname'], details['lname'],"student",details['email'],details['password'],))
    app.mysql.connection.commit()
    cur.close()