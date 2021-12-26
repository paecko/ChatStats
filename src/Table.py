from src.Utils.General import create_value_formatters
import csv

class Table (object):
    def __init__(self, cursor, conversation_id, create_new):
        self.cursor = cursor
        self.conversation_id = conversation_id
        self.table_name = self.conversation_id.replace("-", "")
        self.create_new = create_new

    def insert_in_table(self, fields_to_values):
        values = tuple(fields_to_values.values())
        fields = str(tuple(fields_to_values.keys()))
        fields = fields.replace("'", "")
        formatters = create_value_formatters(len(values))
        insert_statement = """INSERT INTO %s %s VALUES (%s)""" % (self.table_name, fields, formatters)
        self.cursor.execute(insert_statement, values)

    def query_table(self, template_query):
        query = template_query.substitute(table_name=self.table_name)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    @classmethod
    def load_json_in_tables(cls, signal_json_data, *args):
        # load data into any number of table from json_data
        for message in signal_json_data:
            for table in args:
                table.load_table(message)

    @classmethod
    def set_users(cls, *args, uuid_to_name=None, csv_file = None):
        for table in args:
            table.uuid_to_name = {}
            if csv_file == None:
                table.uuid_to_name = uuid_to_name
            else:
                table.uuid_to_name = Table.load_users_from_csv(csv_file)
            # sorting b/c our queries will be sorting the uuids and this dict will be used to cross-check between query results
            table.uuid_to_name = dict(sorted(table.uuid_to_name.items()))

    def get_names_list(self):
        names = []
        for uuid in self.uuid_to_name:
            names.append(self.uuid_to_name[uuid])
        return names
    
    @classmethod
    def load_users_from_csv(cls, csv_file):
        uuid_to_name = {}
        with open(csv_file) as opened_csv_file:
            csv_reader = csv.reader(opened_csv_file)
            for row in csv_reader:
                uuid_to_name[row[0]] = row[1]
        return uuid_to_name
        
    