from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class Jwt(DataClassJsonMixin):
    """
    A class representing a JSON Web Token."""

    username: str
    time_issued: int
