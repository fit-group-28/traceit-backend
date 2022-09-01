from apidata import generate_api_json
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Dict, Any


@dataclass
class HelloWorld(DataClassJsonMixin):
    greeting: str


def endpoint_hello_world() -> Dict[str, Any]:
    """
    Returns a dictionary containing the greeting.

    Returns:
        A dictionary containing the greeting.
    """
    greeting = HelloWorld(greeting="Hello, World!")

    return generate_api_json(greeting)
