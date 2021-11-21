from SignalJsonMessages import SignalJsonMessages
from MessageDatabase import MessageDatabase
from Utils.load_database import load_database


signalJsonData = SignalJsonMessages("db.sqlite", "config.json")
Database = MessageDatabase()
load_database(Database, signalJsonData)
