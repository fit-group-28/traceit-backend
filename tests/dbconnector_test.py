from src.dbconnector import make_connection, connExecute, connQuery
from psycopg2.extensions import connection


def test_make_connection():
    """
    Tests the make_connection function. Requires the database to be running and ready to receive connections.
    """
    conn = make_connection()
    assert conn is not None
    assert isinstance(conn, connection)


def test_connHelpers():
    """
    Tests the connector helpers with a roundtrip. Requires the database to be running and ready to receive connections.
    """
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL);"
    )
    conn.commit()
    conn.close()

    connExecute([("INSERT INTO test_table (name) VALUES ('test');",)])
    results = connQuery([("SELECT * FROM test_table;",)])
    assert results[0] == [(1, "test")]

    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE test_table;")
    conn.commit()
    conn.close()
