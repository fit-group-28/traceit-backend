from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from flask import Request
from flask_jwt_extended import create_access_token

from apidata import ApiResponse


@dataclass
class Login(DataClassJsonMixin):
    msg: str
    access_token: str = ""


def endpoint_login(request: Request) -> ApiResponse[Login]:
    requestJson = request.json

    if isinstance(requestJson, dict) and validate_password(
        (username := requestJson.get("username", None)),
        requestJson.get("password", None),
    ):
        access_token = create_access_token(identity=username)
        apiResponse = ApiResponse(
            response=Login(msg="Authentication success", access_token=access_token),
            statusCode=200,
        )
    else:
        apiResponse = ApiResponse(
            response=Login(msg="Authentication failure"), statusCode=401
        )

    return apiResponse


def validate_password(username: str, password: str) -> bool:
    """
    Validate a username and password.

    Args:
        username: The username to validate.
        password: The password to validate.

    Returns:
        True if the username and password are valid, False otherwise.
    """
    return (
        username is not None
        and password is not None
        and username == "test"
        and password == "test"
    )