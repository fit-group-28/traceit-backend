import psycopg2
from typing import Tuple, Iterable, List


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
            cursor.execute(*action)
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
            cursor.execute(*query)
            results.append(cursor.fetchall())
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        conn.close()
        print(error)
        raise error

    return results


def make_connection() -> psycopg2.extensions.connection:
    """
    Make a connection to the database.
    """
    return psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
    )
