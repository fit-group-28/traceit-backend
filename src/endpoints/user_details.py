from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from apidata import ApiData, ApiResponse
from userjwt import Jwt
from dbconnector import connQuery


@dataclass
class UserDetails(DataClassJsonMixin):
    """
    A class representing the data of a response to a user details request.

    Attributes:
        username: The username of the user.
        time_issued: The time the user's token was issued.
        email: The email of the user.
    """

    uid: str
    username: str
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

        try:
            fetchUser = connQuery(
                [
                    (
                        'SELECT id, username, email FROM "User" WHERE username = %s',
                        (user_jwt.username,),
                    )
                ]
            )

            uid, username, email = fetchUser[0][0]
            uid, username, email = uid.strip(), username.strip(), email.strip()

            apiResponse = ApiResponse(
                response=ApiData(
                    data=UserDetails(
                        uid=uid,
                        username=username,
                        email=email,
                    )
                ),
                statusCode=200,
            )

        except Exception as e:
            apiResponse = ApiResponse(
                response=UserDetailsFailure(msg="Database error"),
                statusCode=500,
            )

    return apiResponse
