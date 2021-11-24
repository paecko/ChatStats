from Utils.General import create_value_formatters
from Table import Table


class ReactionsTable(Table):
    def __init__(self, cursor, conversation_id):
        super().__init__(cursor, conversation_id)
        self.conversation_id = conversation_id
        self.table_name = "Reactions" + self.conversation_id.replace("-", "")
        self.cursor.execute("DROP TABLE IF EXISTS %s" % self.table_name)
        self.cursor.execute("CREATE TABLE %s (emoji TEXT, fromId TEXT, targetAuthorUuid TEXT)" % self.table_name)

    def load_table(self, message):
        if 'reactions' in message:
            for reaction in message['reactions']:
                self.insert_in_table({"emoji": reaction['emoji'], "fromId":reaction['fromId'], "targetAuthorUuid":reaction['targetAuthorUuid']})
        