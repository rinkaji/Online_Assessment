import os 
class Config:
    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'root'
    MYSQL_PORT = 3306
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'online_assessment'
    SECRET_KEY = os.urandom(24)
