from src.endpoints.login import validate_password
from src.endpoints.user_regist import create_user
from tests.helper import delete_user
import pytest


def test_validate_password():
    delete_user("login_user")  # clean up just in case

    # create user
    assert create_user("login_user", "password", "test@gmail.com")

    # validate password
    assert validate_password("login_user", "password")
    assert not validate_password("login_user", "password2")

    # delete user
    delete_user("login_user")
