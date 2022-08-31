from typing import Tuple


def show_all_db_users() -> Tuple[str]:
    """
    Show all users in the database.
    """
    return ("SELECT * FROM user;",)
