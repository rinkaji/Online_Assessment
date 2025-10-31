import MySQLdb.cursors
import app as app

def find_account(email):
    cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users where email = %s AND role = %s", (email, 'instructor'))
    data = cur.fetchone()
    cur.close()
    return data
