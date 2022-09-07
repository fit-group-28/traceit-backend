from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from apidata import ApiData, ApiResponse


@dataclass
class HelloWorld(DataClassJsonMixin):
    """
    A class representing the data of a response to a hello world request.

    Attributes:
        greeting: The greeting message to provide in the response."""

    greeting: str


def endpoint_hello_world() -> ApiResponse[ApiData[HelloWorld]]:
    """
    Returns a response to a hello world request.

    Returns:
        A response to the hello world request.
    """
    greeting = HelloWorld(greeting="Hello, World!")

    apiData = ApiData(data=greeting)
    return ApiResponse(response=apiData, statusCode=200)
