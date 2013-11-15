#!/usr/bin/python

#
# This tool converts notes from
# Samsung's Memo Android-App
# to different formats:
#  Text
#  Lymbo-XML 
#  JSON
#

export = "Lymbo"

from sys import argv, exit, stdout
from datetime import datetime

# requires SQLite 3.x
try:
    import sqlite3
except ImportError:
    print "Requires SQLite library. Please install python-sqlite."
    exit()

def strUnixTime(unixtime):
    return datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')+' GMT'

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
class Memo:
    def __init__(self, row):
        self.id = row[0]
        self.title = row[1]
        self.content = row[2]
        self.color = row[3]
        self.modify_t = row[4]/1000.
        self.create_t = row[5]/1000.

def Memos(dbfile):
    db = sqlite3.connect(dbfile)
    dbcursor = db.cursor()
    results = dbcursor.execute('SELECT * FROM memo')
    return [Memo(row) for row in results]

if export == 'JSON':
    stdout.write('{\n')
    comma = False
    for memo in Memos(dbfile):
        if comma:
            stdout.write(',\n')
        comma = True
        stdout.write("\t'"+strUnixTime(memo.create_t)+"': '"+memo.content.replace('\n','\\n').encode('ascii', 'xmlcharrefreplace')+"'")
    stdout.write('\n}')

elif export == 'Lymbo':
    stdout.write("""<?xml version="1.0" encoding="UTF-8"?>\n
<lymbo>
<text>Notes from Samsung Memo App</text>
<stack>
""")
    for memo in Memos(dbfile):
        stdout.write("""\t<card>
\t\t<title>"""+strUnixTime(memo.create_t)+"""</title>
\t\t<front>
\t\t\t<text>"""+memo.content.replace('\n','\\n').encode('ascii', 'xmlcharrefreplace')+"""</text>
\t\t</front>
\t</card>
""")
    
    stdout.write("""</stack>
</lymbo>
""")
