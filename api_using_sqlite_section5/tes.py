import sqlite3

connector = sqlite3.connect('data.db')

cursor = connector.cursor()
#create_table = "CREATE TABLE users(id int, username text, password text)"
#cursor.execute(create_table)

#user = (1 , 'Jose', 'Jose')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
#cursor.execute(insert_query, user)

users = [(2, 'rolf', 'rolf'), (3, 'test', 'test')]

cursor.executemany(insert_query, users)
connector.commit()
connector.close()