from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import TypeVar, Generic, Tuple, Dict, Any


A = TypeVar("A", bound=DataClassJsonMixin)


@dataclass
class ApiResponse(Generic[A]):
    """
    A class representing an API response.

    Attributes:
        response: The response data.
        statusCode: The status code of the response."""

    response: A
    statusCode: int

    def response_tuple(self) -> Tuple[Dict[str, Any], int]:
        """
        Returns the response as a tuple.

        Returns:
            The response as a tuple."""
        return self.response.to_dict(), self.statusCode


@dataclass
class ApiData(DataClassJsonMixin, Generic[A]):
    """
    A class representing the data of an API response.

    Attributes:
        data: The data of the response."""

    data: A


@dataclass
class JwtFailure(DataClassJsonMixin):
    """
    A class representing a JWT failure. Usually returned with a 401 status code.

    Attributes:
        msg: The message of the failure."""

    msg: str


def jwt_failure():
    return ApiResponse(
        response=JwtFailure(msg="User not logged in"),
        statusCode=401,
    )


@dataclass
class DbFailure(DataClassJsonMixin):
    """
    A class representing a databse query error. Usually returned with a 500 status code.

    Attributes:
        msg: The message of the failure."""

    msg: str


def db_failure(e: Exception):
    return ApiResponse(
        response=DbFailure(msg="Database query error: " + str(e)),
        statusCode=500,
    )
