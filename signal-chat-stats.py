import argparse
from src.SignalJsonMessages import SignalJsonMessages
from src.MessageTable import MessageTable
from src.ReactionsTable import ReactionsTable
from src.DatabaseCursor import DatabaseCursor
from src.Table import Table
import json
import os

STATS_IMAGES_PATH = "stats/"


parser = argparse.ArgumentParser(description='Create and saves stats images based on a group chat in a signal sql database')
subparsers = parser.add_subparsers()

parser_generate = subparsers.add_parser("generate", help="Generate and save stats graph for chat of given conversationId")
parser_generate.add_argument("conversationId", type=str, help="conversationId of group chat or personal chat.")
parser_generate.add_argument("users", type=str, help="users csv path")
parser_generate.add_argument("-j", "--json", type=str, help="path of extracted json file to be used for generating stats.", default="data.json")

parser_extract = subparsers.add_parser("extract", help="Extract data from signal db and output to json file.")
parser_extract.add_argument("database", type=str, help="db.sqlite path")
parser_extract.add_argument("config", type=str, help="config.json path")
parser_extract.add_argument("-n", "--name", type=str, help="Name of output json file", default="data.json")
parser_extract.add_argument("-i", "--info", type=bool, help="Get key information that will help figuring out conversationId and user Id", default=True)


args = parser.parse_args()
MESSAGE_DISPLAY_COUNT = 4
def extract_key_information(signalJsonMessages):
    result = {}
    for message in signalJsonMessages:
        if 'conversationId' in message and 'body' in message and 'sourceUuid' in message:
            conversation_id = message['conversationId']
            source_uuid = message['sourceUuid']
            body = message['body']

            if conversation_id not in result:
                result[conversation_id] = {}
            if source_uuid not in result[conversation_id]:
                result[conversation_id][source_uuid] = []
            if len(result[conversation_id][source_uuid]) < MESSAGE_DISPLAY_COUNT:
                result[conversation_id][source_uuid].append(body)
    return result


def extract(database, config, file_name):
    config_to_sqlite = {config:database}
    return SignalJsonMessages(config_to_sqlite, create_json_file=True, file_name=file_name)


def format_key_info(key_info):
    formatted_info = ""
    conv_no = 1
    for conv_id in key_info:
        formatted_info += str(conv_no) + ". conversationId: " + conv_id + "\n\n" + "\t" + "UserIds:"
        user_id_no = 1
        for user_id in key_info[conv_id]:
            formatted_info += "\n\t" + str(user_id_no) + ". " + user_id + "=" + str(key_info[conv_id][user_id]) + "\n"
            user_id_no += 1
        conv_no += 1
        formatted_info += "\n\n"

    return formatted_info

if "database" in args and "config" in args:
    signalJsonMessages = extract(args.database, args.config, args.name)
    if args.info == True:
        res = extract_key_information(signalJsonMessages)
        formatted = format_key_info(res)
        with open("keyinfo.txt", 'w') as file:
            file.write(formatted)

if "conversationId" in args and "users" in args and "json" in args:
    with open(args.json, "r") as file:
        signalJsonData = json.load(file)

    cursor = DatabaseCursor("ChatData")
    messageTable = MessageTable(cursor, args.conversationId, create_new = True)
    reactionTable = ReactionsTable(cursor, args.conversationId, create_new = True)

    Table.load_json_in_tables(signalJsonData, messageTable, reactionTable)
    Table.set_users(messageTable, reactionTable, csv_file="Users.csv")

    if not os.path.isdir(STATS_IMAGES_PATH):
        os.makedirs(STATS_IMAGES_PATH)
        
    messageTable.plot_messages_per_user(save_to=STATS_IMAGES_PATH + "msgcounts.png")
    reactionTable.plot_received_user_reactions(save_to=STATS_IMAGES_PATH + "user-reacts.png")
    reactionTable.plot_receieved_reactions_percentages(message_table=messageTable, save_to=STATS_IMAGES_PATH + "user-reacts-percentages.png")