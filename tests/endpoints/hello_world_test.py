from src.endpoints.hello_world import endpoint_hello_world
from src.userjwt import Jwt


def test_hello_world():
    """
    Tests the hello world endpoint.
    """
    response = endpoint_hello_world(None)
    assert response.response_tuple() == ({"data": {"greeting": "Hello, World!"}}, 200)


def test_hello_world_with_jwt():
    """
    Tests the hello world endpoint with a JWT.
    """
    response = endpoint_hello_world(Jwt(username="test", time_issued=1234567890))
    assert response.response_tuple() == (
        {"data": {"greeting": "Hello, test. Your token was created at 1234567890!"}},
        200,
    )
