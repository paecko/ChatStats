import sqlite3

class DatabaseCursor:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name + ".db")
        self.cursor = self.connection.cursor()

    def execute(self, statement, values=None):
        if values is None:
            self.cursor.execute(statement)
        else:
            self.cursor.execute(statement, values)
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()    
    