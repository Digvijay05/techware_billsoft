import sqlite3

conn = sqlite3.connect("DB\\Business.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE DESIGNATION")

sql = """CREATE TABLE IF NOT EXISTS DESIGNATION(
                               id  INTEGER PRIMARY KEY autoincrement,
                               designation VARCHAR(500) NOT NULL)"""

cursor.execute(sql)
sql1 = """INSERT INTO DESIGNATION(designation) VALUES(?)"""
cursor.execute(sql1, ("Store Manager",))
cursor.execute(sql1, ("Store Executive",))
cursor.execute(sql1, ("Logistics Executive",))

cursor.execute("SELECT * FROM DESIGNATION")
print(cursor.fetchall())

conn.commit()
conn.close()
print("done")
conn = sqlite3.connect("DB\\Employee.db")
cursor = conn.cursor()

conn = sqlite3.connect("DB\\Items.db")
cursor = conn.cursor()

conn = sqlite3.connect("DB\\Business.db")
cursor = conn.cursor()
# cursor.execute("DROP TABLE Category")
sql = """CREATE TABLE IF NOT EXISTS CATEGORY(
                               id  INTEGER PRIMARY KEY autoincrement,
                               Category VARCHAR(500) NOT NULL)"""
cursor.execute(sql)

conn = sqlite3.connect("DB\\Business.db")
cursor = conn.cursor()
# cursor.execute("DROP TABLE EXPENSE")
sql = """CREATE TABLE IF NOT EXISTS EXPENSE(
                               id  INTEGER PRIMARY KEY autoincrement,
                               Expense VARCHAR(500) NOT NULL)"""
cursor.execute(sql)

conn = sqlite3.connect("DB\\Business.db")
cursor = conn.cursor()
# cursor.execute("DROP TABLE EXPENSE")
sql = """CREATE TABLE IF NOT EXISTS UNIT(
                               id  INTEGER PRIMARY KEY autoincrement,
                               Unit VARCHAR(500) NOT NULL)"""
cursor.execute(sql)
