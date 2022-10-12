from src.endpoints.user_details import userDetailsQuery
from src.endpoints.user_regist import create_user
from tests.helper import delete_user
import pytest


def test_userDetailsQuery():
    """
    Tests the userDetailsQuery function, which queries the database for a user's details.
    """
    delete_user("details_user")  # clean up just in case

    # create user
    assert create_user("details_user", "password", "test@gmail.com")

    # query user
    _, username, email = userDetailsQuery("details_user")

    assert username == "details_user"
    assert email == "test@gmail.com"

    with pytest.raises(Exception):
        userDetailsQuery("asdhfasf")

    # delete user
    delete_user("details_user")
