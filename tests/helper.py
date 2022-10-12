from src.dbconnector import connExecute


def delete_user(username: str):
    """
    Deletes a user from the database.

    Args:
        username: The username of the user to delete.

    Returns:
        True if the user was deleted successfully.
    """

    # delete user
    dbOps = [
        ('DELETE FROM "User" WHERE username = %s;', (username,)),
        (
            'DELETE FROM "UserCredentials" WHERE id = (SELECT id FROM "User" WHERE username = %s);',
            (username,),
        ),
    ]

    connExecute(dbOps)
