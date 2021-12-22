import argparse

parser = argparse.ArgumentParser(description='Create and saves stats images based on a group chat in a signal sql database')

# essentials: path to db, path to config, conversationId, path to Users.csv

subparsers = parser.add_subparsers(help='sub-command help')

parser_generate = subparsers.add_parser("generate", help="Generate and save stats graph for chat of given conversationId")

parser_generate.add_argument("database", type=str, help="database path")
parser_generate.add_argument("config", type=str, help="config path")
parser_generate.add_argument("conversationId", type=str, help="conversationId of group chat or personal chat.")
parser_generate.add_argument("users", type=str, help="users csv path")



args = parser.parse_args()
print(args)
