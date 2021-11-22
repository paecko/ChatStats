import sqlite3
from Utils.General import are_required_parameters_in_message, unix_time_to_date_time_string


REQUIRED_PARAMETERS = ['timestamp', 'sourceUuid', 'body', 'conversationId']


class MessageDatabase:
    @classmethod
    def get_required_parameters(cls):
        return REQUIRED_PARAMETERS

    def __init__(self, conversation_id):
        self.connection = sqlite3.connect("SignalChatData.db")
        self.cursor = self.connection.cursor()
        self.conversation_id = conversation_id
        # remove dashes as they are invalid characters for table name
        self.table_name = "Messages " + self.conversation_id.replace("-", "")
        self.cursor.execute("DROP TABLE IF EXISTS %s" % self.table_name)
        self.cursor.execute("CREATE TABLE %s (timestamp text, source_uuid TEXT, body TEXT)" % self.table_name)
    
    def load_database_with_json_messages(self, json_obj):
        for message in json_obj:
            if are_required_parameters_in_message(message, REQUIRED_PARAMETERS) and message['conversationId'] == self.conversation_id:
                timestamp_string = unix_time_to_date_time_string(message['timestamp'])
                # create tuple of essential values
                extracted_message_values = (timestamp_string, message['sourceUuid'], message['body'])
                # prepare insert statement
                formatters = self.create_value_formatters(extracted_message_values)
                insert_statement = """INSERT INTO %s (timestamp, source_uuid, body) VALUES (%s)""" % (self.table_name, formatters)
                self.insert(insert_statement, extracted_message_values)

        self.close_connection()
        

    def create_value_formatters(self, values):
        '''
        Replace each value with a question mark.
        Eg: ("241", "2", "yo") -> (?,?,?)
        '''
        formatters = "?" * len(values)
        formatters = ",".join(formatters)
        return formatters


    def insert(self, insert_statement, values):
        self.cursor.execute(insert_statement, values)
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

    def __str__(self):
        return self.table_name



    ''' general insert statement
    def insert(self, fields:list, values:list):
        query_statement = """INSERT INTO %s """ %  self.table_name
        fields_str = "(" + ','.join(fields) + ") "

        for index, value in enumerate(values):
            values[index] = '"' + value + '"'
        values_str = "VALUES (" + ','.join(values) + ")"

        query_statement += fields_str + values_str
        self.cursor.execute(query_statement)
        self.connection.commit() 
    '''

