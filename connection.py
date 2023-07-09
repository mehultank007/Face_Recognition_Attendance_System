import sqlite3
from datetime import datetime
conn = sqlite3.connect("studentdb")
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS students(
        stid INTEGER PRIMARY KEY AUTOINCREMENT,
        stname VARCHAR(50),
        stclass VARCHAR(10)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS cs(
        idx INTEGER  PRIMARY KEY AUTOINCREMENT,
        stid INTEGER,
        stdate REAL,
        CONSTRAINT fk_stid FOREIGN KEY (stid) REFERENCES students(stid)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS java(
        idx INTEGER  PRIMARY KEY AUTOINCREMENT,
        stid INTEGER,
        stdate REAL,
        CONSTRAINT fk_stid FOREIGN KEY (stid) REFERENCES students(stid)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS sad(
        idx INTEGER  PRIMARY KEY AUTOINCREMENT,
        stid INTEGER,
        stdate REAL,
        CONSTRAINT fk_stid FOREIGN KEY (stid) REFERENCES students(stid)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS os(
        idx INTEGER  PRIMARY KEY AUTOINCREMENT,
        stid INTEGER,
        stdate REAL,
        CONSTRAINT fk_stid FOREIGN KEY (stid) REFERENCES students(stid)
    )
''')

arg1 = 1
arg2 = 'Meet Vadhiya'
arg3 = 'BCA SEM 4'
current_dt = str(datetime.now().strftime('%d/%m/%Y')) 

# var = "INSERT INTO subject (stid,cs,jv,se,os) VALUES (?,?,?,?,?);"
# cur.execute(var,(s, current_dt, current_dt, current_dt, current_dt))

# var = "INSERT INTO students (stid,stname,stclass,stdate)  VALUES (?,?,?,?);"
# print(var)
# cur.execute(var,(arg1,arg2,arg3,current_dt))
# for row in cur.execute('''SELECT * FROM students '''):
#     print(row)
