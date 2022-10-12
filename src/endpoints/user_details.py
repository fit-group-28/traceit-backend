from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from src.apidata import (
    ApiData,
    ApiResponse,
    JwtFailure,
    DbFailure,
    jwt_failure,
    db_failure,
)
from src.userjwt import Jwt
from src.dbconnector import connQuery

from typing import Tuple


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


def endpoint_user_details(
    user_jwt: Jwt | None,
) -> ApiResponse[ApiData[UserDetails] | JwtFailure | DbFailure]:
    """
    Returns a response to a hello world request.

    Returns:
        A response to the hello world request.
    """
    if not user_jwt:
        return jwt_failure()

    try:
        uid, username, email = userDetailsQuery(user_jwt.username)
        return ApiResponse(
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
        return db_failure(e)


def userDetailsQuery(username: str) -> Tuple[str, str, str]:
    """
    Performs the database query for user details.

    Returns:
        A response to the hello world request.
    """

    getUserDetailsQuery = [
        (
            'SELECT id, username, email FROM "User" WHERE username = %s',
            (username,),
        )
    ]
    fetchUser = connQuery(getUserDetailsQuery)

    uid, username, email = fetchUser[0][0]
    return uid.strip(), username.strip(), email.strip()
