import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

user = (1, "will", "password123")

insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
  (2, "tyler", "password456"),
  (3, "huck", "password789")
]

select_query = "SELECT * FROM users"

cursor.executemany(insert_query, users)
for row in cursor.execute(select_query):
  print(row)

connection.commit()

connection.close()