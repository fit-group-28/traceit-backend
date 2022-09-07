from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from apidata import ApiData, ApiResponse


@dataclass
class HelloWorld(DataClassJsonMixin):
    greeting: str


def endpoint_hello_world() -> ApiResponse[HelloWorld]:
    """
    Returns a dictionary containing the greeting.

    Returns:
        A dictionary containing the greeting.
    """
    greeting = HelloWorld(greeting="Hello, World!")

    apiData = ApiData(data=greeting)
    return ApiResponse(response=apiData, statusCode=200)
