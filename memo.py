#!/usr/bin/python

#
# This tool converts notes from
# Samsung's Memo Android-App
# to different formats:
#  Text
#  Lymbo-XML 
#  JSON
#

from sys import argv, exit

# requires SQLite 3.x
try:
    import sqlite3
except ImportError:
    print "Requires SQLite library. Please install python-sqlite."
    exit()

# ./memo.py "Memo.db"
dbfile = 'Memo.db'
if len(argv) > 1:
    dbfile = argv[1]

#
# Database "Memo.db":
#
# Table "memo" fields:
#  INT  id
#  TEXT title
#  TEXT content
#  INT  color
#  INT  modify_t
#  INT  create_t
#

db = sqlite3.connect(dbfile)
dbcursor = db.cursor()
results = dbcursor.execute('SELECT * FROM memo')
for row in results:
    print row
db.close()
