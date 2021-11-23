import sqlite3
from Utils.General import create_value_formatters

class Table:
    def __init__(self, cursor, table_name="table"):
        self.cursor = cursor
        self.table_name = table_name
        self.cursor.execute("DROP TABLE IF EXISTS %s" % self.table_name)
        self.cursor.execute("CREATE TABLE %s (timestamp text, source_uuid TEXT, body TEXT)" % self.table_name)


    def insert_in_table(self, fields_to_values):
        values = tuple(fields_to_values.values())
        fields = str(tuple(fields_to_values.keys()))
        fields = fields.replace("'", "")
        formatters = create_value_formatters(len(values))
        insert_statement = """INSERT INTO %s %s VALUES (%s)""" % (self.table_name, fields, formatters)
        self.cursor.execute(insert_statement, values)
        

    