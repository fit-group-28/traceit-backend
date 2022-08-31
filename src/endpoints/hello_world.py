from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from utils import copyToJson


@dataclass
class HelloWorld(DataClassJsonMixin):
    data: str


def hello_world():
    hw = HelloWorld(data="Hello, World!")

    return copyToJson(hw)
