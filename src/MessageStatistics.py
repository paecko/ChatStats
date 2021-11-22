import sqlite3

from MessageDatabase import MessageDatabase
from Utils.General import date_time_string_to_object


class MessageStatistics:
    def __init__(self, message_db: MessageDatabase):
        self.message_db = message_db

    def get_overall_stats(self):
        total_messages = self.get_number_of_total_messages
        messages_per_day = self.get_messages_per_day
        
    def get_number_of_total_messages(self):
        total_message_statement = "SELECT COUNT(*) FROM %s" % self.message_db
        return self.message_db.execute_query(total_message_statement)

    def get_messages_per_day(self, total_messages):
        return total_messages//self.get_chat_length_in_days()

    def get_chat_length_in_days(self):
        oldest_message_timestamp_query = "SELECT * FROM messages ORDER BY timestamp ASC LIMIT 1"
        latest_message_timestamp_query = "SELECT * FROM messages ORDER BY timestamp DESC LIMIT 1"
                
        oldest_message_timestamp = self.message_db.execute_query(oldest_message_timestamp_query)
        latest_message_timestamp = self.message_db.execute_query(latest_message_timestamp_query)

        oldest_message_object = date_time_string_to_object(oldest_message_timestamp)
        latest_message_object = date_time_string_to_object(latest_message_timestamp)

        return (latest_message_object - oldest_message_object).days





