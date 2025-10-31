import app as app
import MySQLdb.cursors

def getAllUsers(role):
    cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users where role = %s", (role,))
    data = cur.fetchall()
    cur.close()
    return data

def deleteUser(id):
    cur = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE from users where id = %s", (id,))
    app.mysql.connection.commit()
    cur.close()
    