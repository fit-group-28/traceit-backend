from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from apidata import ApiData, ApiResponse
from userjwt import Jwt


@dataclass
class UserDetails(DataClassJsonMixin):
    """
    A class representing the data of a response to a user details request.

    Attributes:
        username: The username of the user.
        time_issued: The time the user's token was issued.
        email: The email of the user.
    """

    username: str
    time_issued: int
    email: str


@dataclass
class UserDetailsFailure(DataClassJsonMixin):
    msg: str


def endpoint_user_details(
    user_jwt: Jwt | None,
) -> ApiResponse[ApiData[UserDetails] | UserDetailsFailure]:
    """
    Returns a response to a hello world request.

    Returns:
        A response to the hello world request.
    """
    if not user_jwt:
        apiResponse = ApiResponse(
            response=UserDetailsFailure(msg="User not logged in"),
            statusCode=401,
        )
    else:
        apiResponse = ApiResponse(
            response=ApiData(
                data=UserDetails(
                    username=user_jwt.username,
                    time_issued=user_jwt.time_issued,
                    email=user_jwt.email,
                )
            ),
            statusCode=200,
        )

    return apiResponse
