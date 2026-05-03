import sqlite3

# make the connection
connection = sqlite3.connect("sqlite.db")

cursor = connection.cursor()

#####CREATE TABLE

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS  shipments(
#         id INTEGER,
#         content TEXT,
#         weight REAL,
#         status TEXT
#     )
# """)

#####INSERT DATA
# cursor.execute("""
#     INSERT INTO shipments
#     VALUES (12703,'TV', 12, 'placed')
# """)


#####FETCH DATA
# this will get the reference to first object(cursor),
cursor.execute("""
    SELECT * FROM shipments 
""")

# this will fetch all the rows
data = cursor.fetchall()
# data = cursor.fetchmany(2)
print(data)


#####UPDATE DATA
cursor.execute("""
    UPDATE shipments SET status = 'in_transit'
    WHERE id=12701
""")

connection.commit()

# close the connection when we are done
connection.close()
