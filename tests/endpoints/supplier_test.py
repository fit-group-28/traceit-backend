# test for supplier endpoint
from src.endpoints.supplier import (
    get_supplier
)
from src.endpoints.user_regist import create_user
from tests.helper import delete_user
from src.dbconnector import connExecute
import pytest

def test_getsupplier():
    """
    Tests the get_supplier function, which queries the database for a supplier.
    """
    # create user
    create_user("inv_user", "password", "test@email.com")
    resp = get_supplier()
    assert len(resp) == 3