# signal-chat-stats

A CLI that allows you to generate graphs for various metrics based on a Signal group conversation.

## Getting Started

You will need the Signal sqlite database which you can find in:  
```Mac: ~/Library/Application Support/Signal/sql/db.sqlite```.    
```Windows: C:\Users\<YourName>\AppData\Roaming\Signal\sql\db.sqlite```

To decrypt the data in db.sqlite, you will need the decryption key found at:  
```~/.../Signal/config.json```

## Dependencies
```
python3 -m pip install matplotlib pandas
```

## Usage

signal-chat-stats.py is a CLI used to generate images for various stats. There are two steps to this process.  
Start with the extract command

```
$ python3 generate_stats.py extract signal/sql/db.sqlite signal/config.json

Options include:
  -n NAME, --name NAME  Name of output json file
  -i INFO, --info INFO  Get key information that will help figuring out conversationId and user Id
```
This will create a keyinfo.txt file which lists out the conversationIds of all the private and group conversations.  
Under each conversationId is a list of userIds of the members of that conversation. Followed by a sample of 4 messages for each user in that conversation.

This is helpful since the command for generating the stats requires the arguments 'conversationId' and 'Users.csv'. The latter is formatted as:  
```
<userid>,<label-name-in-graphs>
```
The keyinfo.txt allows you to track down which conversationId belongs to which chat and the names belonging to the user ids. Do this with Signal client's search feature.  
Another option is to scour through the 'data.json' file created after this command and use that for tracking down conversationIds and User names.

Obviously, this is not a very intutive way. But the signal database does not have a column for conversation-name and user-names.

The next step is simply using the conversationId and Users.csv to generate the stats images in a new relative folder 'stats'.

```
$ export conversationId="928h2c1l-a216-4884-9116-f9e0a0695cv4"
$ python3 generate_stats.py generate $conversationId myResources/Users.csv
```

