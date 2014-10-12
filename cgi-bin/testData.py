#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('helpMe_DB.db')

#conn.execute('''INSERT INTO USERS VALUES('','');''')

#----making users---
conn.execute('''INSERT INTO USERS VALUES('john01');''')
conn.execute('''INSERT INTO USERS VALUES('john02');''')
conn.execute('''INSERT INTO USERS VALUES('john03');''')		

#----making skill---
conn.execute('''INSERT INTO SKILLS VALUES('john01','COMP1917');''')
conn.execute('''INSERT INTO SKILLS VALUES('john01','COMP1927');''')
conn.execute('''INSERT INTO SKILLS VALUES('john02','COMP1917');''')
conn.execute('''INSERT INTO SKILLS VALUES('john02','COMP1927');''')
conn.execute('''INSERT INTO SKILLS VALUES('john02','COMP2041');''')
conn.execute('''INSERT INTO SKILLS VALUES('john03','COMP2041');''')
conn.execute('''INSERT INTO SKILLS VALUES('john03','COMP3331');''')	

#----making job queue---
conn.execute('''INSERT INTO JOB_QUEUE VALUES('500010',datetime('now'),'lisa01','need help with 1917 assignment1','COMP1917','drum08','30','YES','');''')
conn.execute('''INSERT INTO JOB_QUEUE VALUES('500020',datetime('now'),'lisa02','need help with 1917 assignment1','COMP1917','drum09','45','YES','');''')
conn.execute('''INSERT INTO JOB_QUEUE VALUES('500030',datetime('now'),'lisa03','need help with 2041 week04 lab','COMP2041','drum10','15','YES','');''')
conn.commit()

print "made test data";
conn.close()
