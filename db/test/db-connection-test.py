#!/usr/bin/python3

# import the connect library from psycopg2
from psycopg2 import connect

# declare connection instance
conn = connect(
    database="test_database",
    host="0.0.0.0",
    port=5432,
    user="postgres",
    password="postgres",
)
print(conn)
# declare a cursor object from the connection
cursor = conn.cursor()

# execute an SQL statement using the psycopg2 cursor object
cursor.execute("SHOW search_path;")
cursor.execute("select * from user;")
# enumerate() over the PostgreSQL records
for i, record in enumerate(cursor):
    print("\n", type(record))
    print(record)

# close the cursor object to avoid memory leaks
cursor.close()

# close the connection as well
conn.close()
