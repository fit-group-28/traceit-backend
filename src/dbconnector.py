import psycopg2
from psycopg2.extensions import connection
from typing import Tuple, Iterable, List


def make_connection() -> connection:
    """
    Make a connection to the database. Don't call this directly, instead use the provided functions.
    """
    return psycopg2.connect(
        database="test_database",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
    )


def connExecute(actions: Iterable[Tuple[str] | Tuple[str, Tuple]]) -> None:
    """
    Creates a connection and performs an iterable of execution statements on a database atomically.

    Args:
        actions: An iterable of tuples containing the SQL statement and the arguments.

    Returns:
        None

    Raises:
        psycopg2.Error: If an error occurs during the database operation.
    """
    conn = make_connection()
    cursor = conn.cursor()

    try:
        for action in actions:
            first, rest = action[0], action[1:]
            if rest:
                cursor.execute(first, *rest)
            else:
                cursor.execute(first)
        conn.commit()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        conn.close()
        print(error)
        raise error


def connQuery(queries: Iterable[Tuple[str] | Tuple[str, Tuple]]) -> List[Tuple]:
    """
    Creates a connection and performs an iterable of query statements on a database atomically.

    Args:
        queries: An iterable of tuples containing the SQL statement and the arguments.

    Returns:
        A list of tuples containing the results of the query.

    Raises:
        psycopg2.Error: If an error occurs during the database operation."""
    conn = make_connection()
    cursor = conn.cursor()

    results = []

    try:
        for query in queries:
            first, rest = query[0], query[1:]
            if rest:
                cursor.execute(first, *rest)
            else:
                cursor.execute(first)
            results.append(cursor.fetchall())
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        conn.close()
        print(error)
        raise error

    return results
