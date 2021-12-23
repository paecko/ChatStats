# ChatStats

A CLI that allows you to generate graphs for various metrics based on a Signal group conversation.

## Getting Started

You will need the Signal sqlite database which you can find in:
```Mac: ~/Library/Application Support/Signal/sql/db.sqlite```
```Windows: C:\Users\<YourName>\AppData\Roaming\Signal\sql\db.sqlite```

You will also need the config.json from the .../Signal folder, the parent of the sql folder. 
This contains the decryption key and will be used for decrypting the chat data.

## Dependencies
```
python3 -m pip install matplotlib pandas
```

## Usage

The script src/generate_stats.py is a CLI used to generate the stats graphs.
The command and the arguments are:
```positional arguments:
  database              database path
  config                config path
  conversationId        conversationId of group chat or personal chat.
  users                 users csv path
  ```
An example:
```python3 generate_stats.py generate signal/sql/db.sqlite signal/config.json 928h2c1l-a216-4884-9116-f9e0a0695cv4 Users.csv```
The stats images will be generated in the root of generate_stats.py
