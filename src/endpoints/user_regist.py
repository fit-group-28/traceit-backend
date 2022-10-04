from dataclasses import dataclass
import random
import re
from uuid import uuid4
from dataclasses_json import DataClassJsonMixin
from dbconnector import connExecute, connQuery
from flask import Request
from apidata import ApiResponse
from argon2 import PasswordHasher


@dataclass
class Register(DataClassJsonMixin):
    """
    A class representing the data of a response to a register request.

    Attributes:
        msg: The message to provide in the response.
        access_token: The access token if authentication is successful."""

    msg: str


def endpoint_register(request: Request) -> ApiResponse[Register]:
    """
    Handles the endpoint for registering a user.

        Args:
            request: The request object.

        Returns:
            A response to the register request.
    """
    requestJson = request.json

    if isinstance(requestJson, dict) and validate(
        (username := requestJson.get("username", None)),
        password := requestJson.get("password", None),
        email := requestJson.get("email", None),
    ):
        try:
            create_user(username, password, email)
            apiResponse = ApiResponse(
                response=Register(msg="Registration success"),
                statusCode=200,
            )
        except Exception:
            apiResponse = ApiResponse(
                response=Register(msg="Registration failure"), statusCode=401
            )

    else:
        apiResponse = ApiResponse(
            response=Register(msg="Invalid credentials format"), statusCode=401
        )

    return apiResponse


def create_user(username: str, password: str, email: str) -> bool:
    """
    Create a user by adding them to the database.
    """

    ph = PasswordHasher()

    # random generated salt
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = [random.choice(ALPHABET) for _ in range(16)]
    salt = "".join(chars)

    # hash the password with the salt
    hashed_password = ph.hash(password.join(salt))
    user_id = str(uuid4())

    # insert the user into the database
    dbOps = [
        (
            'INSERT INTO "User" (id, username, email) VALUES (%s,%s,%s);',
            (user_id, username, email),
        ),
        (
            'INSERT INTO "UserCredentials" (id, salt, password) VALUES (%s,%s,%s);',
            (user_id, salt, hashed_password),
        ),
    ]
    connExecute(dbOps)

    return True


def validate(username: str, password: str, email: str) -> bool:
    """
    Validate a username and password.

    Args:
        username: The username to validate.
        password: The password to validate.
        email: The email to validate.

    Returns:
        True if the username and password are valid, False otherwise.
    """
    if username is None or password is None or email is None:
        return False

    if len(username) < 3 or len(username) > 20:
        return False

    if len(password) < 8 or len(password) > 20:
        return False

    regex = re.compile(
        r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
    )
    return bool(len(email) >= 3 and len(email) <= 320 and re.fullmatch(regex, email))
