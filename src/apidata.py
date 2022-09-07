from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import TypeVar, Generic, Tuple, Dict, Any


A = TypeVar("A", bound=DataClassJsonMixin)


@dataclass
class ApiResponse(Generic[A]):
    response: A
    statusCode: int

    def response_tuple(self) -> Tuple[Dict[str, Any], int]:
        return self.response.to_dict(), self.statusCode


@dataclass
class ApiData(DataClassJsonMixin):
    data: DataClassJsonMixin
