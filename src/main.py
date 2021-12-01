from SignalJsonMessages import SignalJsonMessages
from MessageDatabase import MessageDatabase
from MessageTable import MessageTable
from ReactionsTable import ReactionsTable
from DatabaseCursor import DatabaseCursor
from Plotter import Plotter
from Table import Table

#signalJsonData = SignalJsonMessages("db-2.sqlite", "config.json")

cursor = DatabaseCursor("Final")

messageTable = MessageTable(cursor, "xx-xxx-", create_new = False)
reactionTable = ReactionsTable(cursor, "xx-xx", create_new=False)

#Table.load_json_in_tables(signalJsonData, messageTable)

reactionTable.set_users(csv_file="Users.csv")
messageTable.set_users(csv_file="Users.csv")
print(reactionTable.plot_receieved_reactions_percentages(messageTable))
#plt = Plotter(reactiontable, None, "Users.csv")
#plt.plot_most_popular_emojis()




