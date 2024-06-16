import sqlite3
def createDb():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
    conn.commit()

def insertData():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
    conn.commit()

# createDb()