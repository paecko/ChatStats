# ChatStats

This library allows one to generate graphs of several metrics from Signal's db.sqlite which can be found in the following locations:

Mac: ~/Library/Application Support/Signal/sql/db.sqlite
Windows: C:\Users\<YourName>\AppData\Roaming\Signal\sql\db.sqlite

## Getting Started

The following explanation is based on code that can be found in src/main.py

Creating a connection to a database that exists. Otherwise, creates a new one.
```
cursor = DatabaseCursor("ChatData")
```



