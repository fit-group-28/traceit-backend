from src.endpoints.login import validate_password
from src.endpoints.user_regist import create_user
from tests.helper import delete_user


def test_sql_injection():
    delete_user("sql_injection")  # clean up just in case

    # create user
    assert create_user("sql_injection", "password", "test@gmail.com")

    # validate password
    assert validate_password("sql_injection", "password")
    assert not validate_password(
        '(SELECT username FROM "User" WHERE username = "sql_injection")', "password"
    )

    # delete user
    delete_user("sql_injection")
