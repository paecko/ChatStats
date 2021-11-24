import sqlite3
from Utils.General import create_value_formatters

class Table (object):
    def __init__(self, cursor, conversation_id):
        self.cursor = cursor
        self.conversation_id = conversation_id
        self.table_name = self.conversation_id.replace("-", "")

    def insert_in_table(self, fields_to_values):
        values = tuple(fields_to_values.values())
        fields = str(tuple(fields_to_values.keys()))
        fields = fields.replace("'", "")
        formatters = create_value_formatters(len(values))
        insert_statement = """INSERT INTO %s %s VALUES (%s)""" % (self.table_name, fields, formatters)
        self.cursor.execute(insert_statement, values)

    def query_table(self, template_query):
        query = template_query.substitute(table_name=self.table_name)
        print(query)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    @classmethod
    def load_json_in_tables(cls, signal_json_data, *args):
        for table in args:
            for message in signal_json_data:
                table.load_table(message)
        
    