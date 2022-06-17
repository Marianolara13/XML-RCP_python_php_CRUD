import mysql.connector

class DateBase:
    def __init__(self):
        self.connection=mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="personal"
        )
        self.cursor=self.connection.cursor()