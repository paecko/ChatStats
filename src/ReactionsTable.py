from Utils.General import are_required_parameters_in_message, sort_by_second
from Table import Table
from string import Template
import matplotlib.pyplot as plt
import pandas as pd


REQUIRED_PARAMETERS = ['reactions', 'conversationId']

class ReactionsTable(Table):
    def __init__(self, cursor, conversation_id, create_new = True):
        super().__init__(cursor, conversation_id, create_new)
        self.conversation_id = conversation_id
        self.table_name = "Reactions" + self.conversation_id.replace("-", "")
        if create_new:
            self.cursor.execute("DROP TABLE IF EXISTS %s" % self.table_name)
            self.cursor.execute("CREATE TABLE %s (emoji TEXT, fromId TEXT, targetAuthorUuid TEXT)" % self.table_name)

    def load_table(self, message):
        if are_required_parameters_in_message(message, REQUIRED_PARAMETERS) and message['conversationId'] == self.conversation_id:
            for reaction in message['reactions']:
                self.insert_in_table({"emoji": reaction['emoji'], "fromId":reaction['fromId'], "targetAuthorUuid":reaction['targetAuthorUuid']})


    def plot_receieved_reactions_percentages(self, message_table, save_to=""):
        self.plot_received_user_reactions(message_table, save_to)

    def plot_received_user_reactions(self, message_table = None, save_to=""):
        key_emojis, count = self.get_most_popular_emojis()
        uuid_to_emoji_counts = self.populate_reaction_counts(key_emojis)
        emoji_counts = self.create_transposed_emoji_counts_list(uuid_to_emoji_counts)
        if message_table is not None:
            self.reaction_percentage_over_total_messages(message_table, emoji_counts)

        data_frame = self.create_reaction_dataframe(key_emojis, emoji_counts)
        names = self.get_names_list()
        df = pd.DataFrame(data_frame, index=names)
        ax = df.plot.bar(rot=0)

        if save_to == "":
            plt.show()
        else:
            plt.savefig(save_to)

    def create_reaction_dataframe(self, key_emojis, emoji_counts):
        data_frame = {}
        for i in range(len(key_emojis)):
            data_frame[key_emojis[i]] = emoji_counts[i]
        return data_frame
    
    def populate_reaction_counts(self, key_emojis):
        query_template = Template("SELECT targetAuthorUuid, emoji, COUNT(*) as count FROM $table_name \
            GROUP BY emoji, targetAuthorUuid ORDER BY targetAuthorUuid, emoji")
        all_user_reaction_counts = self.query_table(query_template)
        uuid_to_emoji_counts = {}

        for user_reaction_count in all_user_reaction_counts:
            uuid, emoji, count = user_reaction_count
            if uuid in self.uuid_to_name and uuid not in uuid_to_emoji_counts:
                uuid_to_emoji_counts[uuid] = self.initialize_emoji_counts(key_emojis)

            if uuid in uuid_to_emoji_counts and emoji in key_emojis:
                uuid_to_emoji_counts[uuid][emoji] = count                
        return uuid_to_emoji_counts

    def initialize_emoji_counts(self, key_emojis):
        # create dict that maps each emoji to a count of 0
        zero_count_emoji_dict = {}
        for emoji in key_emojis:
            zero_count_emoji_dict[emoji] = 0
        # looks like {👍: 0, 😮: 0, ...}
        return zero_count_emoji_dict

    def create_transposed_emoji_counts_list(self, uuid_to_emoji_counts):
        emoji_counts_as_lists = []
        for uuid in uuid_to_emoji_counts:
            emoji_count_list = list(uuid_to_emoji_counts[uuid].values())
            emoji_counts_as_lists.append(emoji_count_list)
        # transpose list so each subarray represents the counts for 1 emoji for every person. 
        # Rather than each subarray representing the counts for each emoji per person.
        emoji_counts = list(map(list, zip(*emoji_counts_as_lists)))
        return emoji_counts


    def get_most_popular_emojis(self):
        query_template = Template("SELECT emoji, COUNT(*) FROM $table_name GROUP BY emoji")
        results = self.query_table(query_template)
        results.sort(key=sort_by_second, reverse=True)
        results = results[:6]
        emojis = [t[0] for t in results]
        counts = [t[1] for t in results]
        return emojis, counts

    def reaction_percentage_over_total_messages(self, message_table, emoji_counts):
        name_to_counts = message_table.get_name_to_message_counts()
        messages_per_user = list(name_to_counts.values())
        for emoji_count_list in emoji_counts:
            for i in range(len(emoji_count_list)):
                print(messages_per_user)
                print(emoji_count_list)
                if messages_per_user[i] != 0:
                    emoji_count_list[i] = (emoji_count_list[i]/messages_per_user[i]) * 100
                else:
                    emoji_count_list[i] = 0
        return emoji_count_list



        
        
