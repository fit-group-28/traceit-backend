from src.apidata import (
    ApiData,
    ApiResponse,
    request_failure,
    RequestFailure,
    JwtFailure,
    DbFailure,
    jwt_failure,
    db_failure,
)
from dataclasses_json import DataClassJsonMixin
from dataclasses import dataclass


@dataclass
class ClassForTests(DataClassJsonMixin):
    msg: str


def test_response_tuple():
    """
    Tests the response_tuple method.
    """
    response = ApiResponse(
        response=ApiData(data=ClassForTests(msg="test")),
        statusCode=200,
    )
    assert response.response_tuple() == ({"data": {"msg": "test"}}, 200)


def test_request_failure():
    """
    Tests the request_failure method.
    """
    response = request_failure("test")
    assert response == ApiResponse(
        response=RequestFailure(msg="Request failure: test"), statusCode=400
    )
    assert response.response_tuple() == ({"msg": "Request failure: test"}, 400)


def test_jwt_failure():
    """
    Tests the jwt_failure method.
    """
    response = jwt_failure()
    assert response == ApiResponse(
        response=JwtFailure(msg="User not logged in"), statusCode=401
    )
    assert response.response_tuple() == ({"msg": "User not logged in"}, 401)


def test_db_failure():
    """
    Tests the db_failure method.
    """
    testException = Exception("test")
    response = db_failure(testException)
    assert response == ApiResponse(
        response=DbFailure(msg="Database query error: test"), statusCode=500
    )
    assert response.response_tuple() == ({"msg": "Database query error: test"}, 500)
