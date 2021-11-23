import sqlite3

class DatabaseCursor:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name + ".db")
        self.cursor = self.connection.cursor()

    def execute(self, *args):
        self.cursor.execute(*args)

    def commit(self):
        self.connection.commit

    