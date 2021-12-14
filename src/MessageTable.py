from Table import Table
from Utils.General import unix_time_to_date_time_string, are_required_parameters_in_message
from string import Template
import matplotlib.pyplot as plt

REQUIRED_PARAMETERS = ['timestamp', 'sourceUuid', 'body', 'conversationId']

class MessageTable(Table):
    def __init__(self, cursor, conversation_id, create_new = True):
        super().__init__(cursor, conversation_id, create_new)
        self.table_name = "Messages" + self.conversation_id.replace("-", "")
        if create_new:
            self.cursor.execute("DROP TABLE IF EXISTS %s" % self.table_name)
            self.cursor.execute("CREATE TABLE %s (timestamp text, source_uuid TEXT, body TEXT)" % self.table_name)

    def load_table(self, message=""):
        if are_required_parameters_in_message(message, REQUIRED_PARAMETERS) and message['conversationId'] == self.conversation_id:
            timestamp_string = unix_time_to_date_time_string(message['timestamp'])
            self.insert_in_table({"timestamp": timestamp_string, "source_uuid":message['sourceUuid'], "body": message["body"]})
    
    def get_messages_per_user(self):
        query_template = Template("SELECT source_uuid, COUNT() as count FROM $table_name GROUP BY source_uuid ORDER BY source_uuid")
        results = self.query_table(query_template)
        counts = []
        for res in results:
            if res[0] in self.uuid_to_name:
                counts.append(res[1])
        return counts 

    def plot_messages_per_user(self, save_to=""):
        message_counts = self.get_messages_per_user()
        names = self.get_names_list()
        print(message_counts)
        print(names)
        plt.bar(names,message_counts)
        plt.tick_params(axis='x', which='major', labelsize=6)
        for index, value in enumerate(message_counts):
            plt.text(index - 0.4,value + 0.01, str(value))
        plt.title("Total Message Count By User")
        if save_to == "":
            plt.show()
        else:
            plt.savefig(save_to)
