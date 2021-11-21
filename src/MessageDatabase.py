import sqlite3
from Utils.General import are_required_parameters_in_message, unix_time_to_date_time_string


REQUIRED_PARAMETERS = ['timestamp', 'sourceUuid', 'body', 'conversationId']


class MessageDatabase:
    @classmethod
    def get_required_parameters(cls):
        return REQUIRED_PARAMETERS

    def __init__(self):
        self.connection = sqlite3.connect("SignalChatData.db")
        self.cursor = self.connection.cursor()
        self.table = "messages"
        self.cursor.execute("DROP TABLE IF EXISTS %s" % self.table)
        self.cursor.execute("CREATE TABLE %s (timestamp text, source_uuid TEXT, body TEXT, conversation_id TEXT)" % self.table)
    
    def load_database_with_json_messages(self, json_obj):
        for message in json_obj:
            if are_required_parameters_in_message(message, REQUIRED_PARAMETERS):
                timestamp_string = unix_time_to_date_time_string(message['timestamp'])
                extracted_message_data = (timestamp_string, message['sourceUuid'], message['body'], message['conversationId'])
                self.insert(extracted_message_data)
        self.close_connection()

    def insert(self, values:tuple):
        placeholder_values = "?" * len(values)
        placeholder_values = ",".join(placeholder_values)
        insert_statement = """INSERT INTO %s (timestamp, source_uuid, body, conversation_id) VALUES (%s)""" % (self.table, placeholder_values)
        self.cursor.execute(insert_statement, values)
        self.connection.commit()

    def close_connection(self):
        self.connection.close()



    ''' general insert statement
    def insert(self, fields:list, values:list):
        query_statement = """INSERT INTO %s """ %  self.table
        fields_str = "(" + ','.join(fields) + ") "

        for index, value in enumerate(values):
            values[index] = '"' + value + '"'
        values_str = "VALUES (" + ','.join(values) + ")"

        query_statement += fields_str + values_str
        self.cursor.execute(query_statement)
        self.connection.commit() 
    '''

