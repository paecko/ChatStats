# ChatStats

This library allows one to generate graphs of several metrics from Signal's db.sqlite which can be found in the following locations:

Mac: ~/Library/Application Support/Signal/sql/db.sqlite
Windows: C:\Users\<YourName>\AppData\Roaming\Signal\sql\db.sqlite

You will also need the config.json file from the Signal folder. This contains the decryption key.

### Getting Started

The following explanation is based on code that can be found in src/main.py

Creating a connection to a database that exists. Otherwise, creates a new one.
```
cursor = DatabaseCursor("ChatData")
```

You will have to create a dictionary mapping config.json to db.sqlite. You can add as many as you want if you have multiple Signal database you want to load and generate stats from. Then simply pass it in to SignalJsonMessages to get the chat data as json objects.
```
config_to_sqlite = {"config.json": "db.sqlite", "config2.json":"db2.sqlite"}
signalJsonData = SignalJsonMessages(config_to_sqlite, create_json_file=True)
```
You might also want to set create_json_file to True for now.

This is where you have to do some manual work. You will need to go through the json data to find the conversationId field representing the group chat or personal chat for which you want to generate stats for. An exmaple is: "928h2c1l-a216-4884-9116-f9e0a0695cv4". You can find this in the data.json file created by SignalJsonMessages.

To be Continued..

            


