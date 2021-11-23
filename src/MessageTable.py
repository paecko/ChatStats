from MessageDatabase import REQUIRED_PARAMETERS
from Table import Table
from Utils.General import unix_time_to_date_time_string, are_required_parameters_in_message, create_value_formatters
from DatabaseCursor import DatabaseCursor

REQUIRED_PARAMETERS = ['timestamp', 'sourceUuid', 'body', 'conversationId']

class MessageTable(Table):
    def __init__(self, cursor, conversation_id):
        self.conversation_id = conversation_id
        self.table_name = "Messages" + self.conversation_id.replace("-", "")
        Table.__init__(cursor, self.table_name)
        self.cursor.execute("CREATE TABLE %s (timestamp text, source_uuid TEXT, body TEXT)" % self.table_name)

    def load_table(self, message=""):
        if are_required_parameters_in_message(message, REQUIRED_PARAMETERS) and message['conversationId'] == self.conversation_id:
            timestamp_string = unix_time_to_date_time_string(message['timestamp'])
            self.insert_in_table({"timestamp": timestamp_string, "fromId":message['sourceUuid'], "body": message["body"]})
      