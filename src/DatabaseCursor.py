import sqlite3


class DatabaseCursor:
    def __new__(cls):
        connection = sqlite3.connect("SignalChatData.db")
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS messages")
        cursor.execute("CREATE TABLE messages (timestamp text, source_uuid TEXT, body TEXT, conversation_id TEXT)")
        return cursor