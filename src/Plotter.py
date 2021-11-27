import csv
import matplotlib.pyplot as plt
from string import Template
from Utils.General import sort_by_second
import pandas as pd
import numpy as np


class Plotter:
    def __init__(self, table, uuid_to_name=None, csv_file = None):
        self.table = table
        self.uuid_to_name = {}
        if csv_file == None:
            self.uuid_to_name = uuid_to_name
        else:
            self.uuid_to_name = self.load_users_from_csv(csv_file)
        self.uuid_to_name = dict(sorted(self.uuid_to_name.items()))
        print(self.uuid_to_name)

    def get_names_list(self):
        names = []
        for uuid in self.uuid_to_name:
            names.append(self.uuid_to_name[uuid])
        return names
    
    def load_users_from_csv(self, csv_file):
        uuid_to_name = {}
        with open(csv_file) as opened_csv_file:
            csv_reader = csv.reader(opened_csv_file)
            for row in csv_reader:
                uuid_to_name[row[0]] = row[1]
        return uuid_to_name

    def plot_most_popular_emojis(self):
        emojis, counts = self.get_most_popular_emojis()

        plt.bar(emojis, counts)
        plt.tick_params(axis='x', which='major', labelsize=6)

        plt.title("Most frequent emojis")
        plt.show()

        
    def create_user_to_emoji_count_dict(self, key_emojis):
        ''' Some users have not reacted with a certain popular emoji.
            Create consistent dict with each emoji set to 0 count.
            So that final pandas dataframe is a working nxn array.
        '''
        # create dict that maps each emoji to a count of 0
        zero_count_emoji_dict = {}
        for emoji in key_emojis:
            zero_count_emoji_dict[emoji] = 0

        # create dict where key is user and zero_count_dict is value which will be updated
        # looks like {👍: 0, 😮: 0, ...}
        return zero_count_emoji_dict
        

    def fill_target_user_reaction_counts(self, key_emojis):
        query_template = Template("SELECT targetAuthorUuid, emoji, COUNT(*) as count FROM $table_name \
            GROUP BY emoji, targetAuthorUuid ORDER BY targetAuthorUuid, emoji")
        target_user_reaction_counts = self.table.query_table(query_template)
        uuid_to_emoji_counts = {}
        for user_reaction_count in target_user_reaction_counts:
            uuid, emoji, count = user_reaction_count
            if uuid in self.uuid_to_name and uuid not in uuid_to_emoji_counts:
                uuid_to_emoji_counts[uuid] = self.create_user_to_emoji_count_dict(key_emojis)

            if uuid in uuid_to_emoji_counts and emoji in key_emojis:
                uuid_to_emoji_counts[uuid][emoji] = count                
        return uuid_to_emoji_counts

    def create_target_user_reaction_dataframe_dict(self):
        key_emojis, count = self.get_most_popular_emojis() 
        uuid_to_emoji_counts = self.fill_target_user_reaction_counts(key_emojis)
        emoji_counts_as_lists = []

        for uuid in uuid_to_emoji_counts:
            emoji_count_list = list(uuid_to_emoji_counts[uuid].values())
            emoji_counts_as_lists.append(emoji_count_list)

        emoji_counts = list(map(list, zip(*emoji_counts_as_lists)))
        data_frame_dict = {}
        for i in range(len(key_emojis)):
            data_frame_dict[key_emojis[i]] = emoji_counts[i]
        return data_frame_dict

    def plot_target_user_reactions(self):
        data_frame_dict = self.create_target_user_reaction_dataframe_dict()
        names = self.get_names_list()
        df = pd.DataFrame(data_frame_dict, index=names)
        ax = df.plot.bar(rot=0)
        plt.show()


    def plot_target_user_reactions_averages(self, message_table):
        key_emojis, count = self.get_most_popular_emojis() 
        uuid_to_emoji_counts = self.fill_target_user_reaction_counts(key_emojis)
        emoji_counts_as_lists = []

        for uuid in uuid_to_emoji_counts:
            emoji_count_list = list(uuid_to_emoji_counts[uuid].values())
            emoji_counts_as_lists.append(emoji_count_list)

        emoji_counts = list(map(list, zip(*emoji_counts_as_lists)))
        print(emoji_counts)
        messages_per_user = self.get_messages_per_user(message_table)
        for emoji_count_list in emoji_counts:
            for i in range(len(emoji_count_list)):
                if messages_per_user[i] != 0:
                    emoji_count_list[i] = (emoji_count_list[i]/messages_per_user[i]) * 100
                    print((emoji_count_list[i]/messages_per_user[i]) * 100)
                else:
                    emoji_count_list[i] = 0
        names = self.get_names_list()

        print(messages_per_user)
        print(names)
        print(emoji_counts)
        data_frame_dict = {}
        print(key_emojis)
        for i in range(len(key_emojis)):
            data_frame_dict[key_emojis[i]] = emoji_counts[i]
        df = pd.DataFrame(data_frame_dict, index=names)
        ax = df.plot.bar(rot=0)
        plt.show()

    def get_messages_per_user(self, message_table):
        query_template = Template("SELECT source_uuid, COUNT() as count FROM $table_name GROUP BY source_uuid ORDER BY source_uuid")
        results = message_table.query_table(query_template)
        counts = []
        for res in results:
            if res[0] in self.uuid_to_name:
                counts.append(res[1])
        return counts 

    def get_most_popular_emojis(self):
        query_template = Template("SELECT emoji, COUNT(*) FROM $table_name GROUP BY emoji")
        results = self.table.query_table(query_template)
        results.sort(key=sort_by_second, reverse=True)
        results = results[:6]
        emojis = [t[0] for t in results]
        counts = [t[1] for t in results]
        return emojis, counts

                 
        


    