from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from src.apidata import ApiData, ApiResponse
from src.userjwt import Jwt


@dataclass
class HelloWorld(DataClassJsonMixin):
    """
    A class representing the data of a response to a hello world request.

    Attributes:
        greeting: The greeting message to provide in the response."""

    greeting: str


def endpoint_hello_world(user_jwt: Jwt | None) -> ApiResponse[ApiData[HelloWorld]]:
    """
    Returns a response to a hello world request.

    Returns:
        A response to the hello world request.
    """
    greeting = (
        HelloWorld(
            greeting=f"Hello, {user_jwt.username}. Your token was created at {user_jwt.time_issued}!"
        )
        if user_jwt
        else HelloWorld(greeting="Hello, World!")
    )

    apiData = ApiData(data=greeting)
    return ApiResponse(response=apiData, statusCode=200)
