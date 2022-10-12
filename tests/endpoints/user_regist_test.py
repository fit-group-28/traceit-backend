from src.endpoints.user_regist import validate, create_user
from src.dbconnector import connExecute
from tests.helper import delete_user


def test_validate():
    """
    Tests the validate function, which checks if a username, password and email are morphologically valid for registration.
    """
    # email
    assert not validate("username", "password", "email")
    assert not validate("username", "password", "email@")
    assert not validate("username", "password", "email@domain.")
    assert not validate("username", "password", "")
    assert not validate("username", "password", "a" * 320 + "@domain.com")

    # username
    assert not validate("", "password", "email@domain.com")
    assert not validate("a", "password", "email@domain.com")
    assert not validate("a" * 21, "password", "email@domain.com")

    # password
    assert not validate("username", "", "email@domain.com")
    assert not validate("username", "a", "email@domain.com")
    assert not validate("username", "a" * 21, "email@domain.com")

    assert validate("username", "password", "email@domain.com")


def test_create_user():
    """
    Tests the create_user function, which creates a user in the database.
    """
    delete_user("regist_user")  # clean up just in case

    # create user
    assert create_user("regist_user", "password", "testemail@email.com")

    # delete user
    delete_user("regist_user")
