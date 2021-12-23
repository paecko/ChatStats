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

args = parser.parse_args()
database = args.database
config = args.config
conversationId = args.conversationId
users = args.users

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
    