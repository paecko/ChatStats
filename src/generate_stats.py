import argparse
from SignalJsonMessages import SignalJsonMessages
from MessageTable import MessageTable
from ReactionsTable import ReactionsTable
from DatabaseCursor import DatabaseCursor
from Table import Table

parser = argparse.ArgumentParser(description='Create and saves stats images based on a group chat in a signal sql database')
subparsers = parser.add_subparsers()
parser_generate = subparsers.add_parser("generate", help="Generate and save stats graph for chat of given conversationId")

parser_generate.add_argument("database", type=str, help="database path")
parser_generate.add_argument("config", type=str, help="config path")
parser_generate.add_argument("conversationId", type=str, help="conversationId of group chat or personal chat.")
parser_generate.add_argument("users", type=str, help="users csv path")
parser_generate.add_argument("-o", "--output", type=str, help="path to where stats images will be saved", default="./")
parser_generate.set_defaults(parser_generate=True)

parser_extract = subparsers.add_parser("extract", help="Extract data from signal db and output to json file.")
parser_extract.add_argument("database", type=str, help="db.sqlite path")
parser_extract.add_argument("config", type=str, help="config.json path")
parser_extract.add_argument("-o", "--output", type=str, help="Location where json output will be stored. Default is root", default="./")


args = parser.parse_args()

def extract(database, config, output="./"):
    config_to_sqlite = {config:database}
    SignalJsonMessages(config_to_sqlite, output=output, create_json_file=True)

if "database" in args and "config" in args:
    extract(args.database, args.config, args.output)
    


'''
cursor = DatabaseCursor("ChatData")
messageTable = MessageTable(cursor, conversationId, create_new = True)
config_to_sqlite = {config:database}
signalJsonData = SignalJsonMessages(config_to_sqlite, create_json_file=False)

messageTable = MessageTable(cursor, conversationId, create_new = True)
reactionTable = ReactionsTable(cursor, conversationId, create_new = True)

Table.load_json_in_tables(signalJsonData, messageTable, reactionTable)
Table.set_users(messageTable, reactionTable, csv_file="Users.csv")

messageTable.plot_messages_per_user(save_to="msgcounts.png")

reactionTable.plot_received_user_reactions(save_to="user-reacts.png")
reactionTable.plot_receieved_reactions_percentages(message_table=messageTable, save_to="user-reacts-percentages.png")
'''
