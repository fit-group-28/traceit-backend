from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
import time

from flask.wrappers import Request
from flask_jwt_extended import create_access_token
from argon2 import PasswordHasher

from src.apidata import ApiResponse
from src.userjwt import Jwt

from src.dbconnector import connQuery


@dataclass
class Login(DataClassJsonMixin):
    """
    A class representing the data of a response to a login request.

    Attributes:
        msg: The message to provide in the response.
        access_token: The access token if authentication is successful."""

    msg: str
    access_token: str = ""


def endpoint_login(request: Request) -> ApiResponse[Login]:
    """
    Handles the endpoint for logging in.

        Args:
            request: The request object.

        Returns:
            A response to the login request.
    """
    requestJson = request.json

    if (
        isinstance(requestJson, dict)
        and "username" in requestJson
        and "password" in requestJson
        and validate_password(
            (username := requestJson["username"]),
            requestJson["password"],
        )
    ):
        access_token = create_access_token(
            identity=Jwt(username=username, time_issued=int(time.time())).to_dict()
        )
        return ApiResponse(
            response=Login(msg="Authentication success", access_token=access_token),
            statusCode=200,
        )

    else:
        return ApiResponse(response=Login(msg="Authentication failure"), statusCode=401)


def validate_password(username: str, password: str) -> bool:
    """
    Validate a username and password.

    Args:
        username: The username to validate.
        password: The password to validate.

    Returns:
        True if the username and password are valid, False otherwise.
    """
    ph = PasswordHasher()

    try:
        fetchHashedCreds = connQuery(
            [
                (
                    'SELECT salt, password FROM "UserCredentials" INNER JOIN "User" ON "UserCredentials".id = "User".id WHERE username = %s',
                    (username,),
                )
            ]
        )
        salt, hashed_pw = fetchHashedCreds[0][0]

        hashed_pw = hashed_pw.strip()
        salt = salt.strip()

        ph.verify(hashed_pw, password.join(salt))
        return True

    except Exception:
        return False
