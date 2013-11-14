#!/usr/bin/python

from sys import exit

try:
    import sqlite3
except:
    print "Requires SQLite library. Please install python-sqlite."
    exit()
    
conn = sqlite3.connect('Memo.db')
c = conn.cursor()
for row in c.execute('SELECT * FROM memo'):
    print row
conn.close()
