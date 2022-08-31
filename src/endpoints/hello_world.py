from dataclasses import dataclass
from dataclasses_json import dataclass_json
import utils


@dataclass_json
@dataclass
class HelloWorld:
    data: str


def hello_world():
    hw = HelloWorld(data="Hello, World!")

    return utils.copyToJson(hw)
