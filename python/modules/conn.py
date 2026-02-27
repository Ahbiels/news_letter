import mysql.connector
from mysql.connector import errorcode
import os

VIEWER_PASSWORD = os.getenv("VIEWER_PASSWORD")

def conn(log):
    try:
        db_conn = mysql.connector.connect(
            host="localhost",
            user="access_viewer",
            passwd=VIEWER_PASSWORD,
        )
        log.info = "Database connection made"
        return db_conn
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist")
        elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("User name or password is wrong")
        else:
            print(error)
    