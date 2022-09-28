from dataclasses import dataclass
import random
import re
from uuid import uuid4
from dataclasses_json import DataClassJsonMixin
import time
from dbconnector import connExecute, connQuery
from flask import Request
from flask_jwt_extended import create_access_token
from apidata import ApiResponse
from userjwt import Jwt
import psycopg2


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
        create_user(username, password, email)
        apiResponse = ApiResponse(response=Register(msg="User created"), statusCode=200)

    else:
        apiResponse = ApiResponse(
            response=Register(msg="User create failure"), statusCode=401
        )

    return apiResponse


def create_user(username: str, password: str, email: str) -> bool:
    """
    Create a user by adding them to the database.
    """
    # random generated salt
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for _ in range(16):
        chars.append(random.choice(ALPHABET))
    salt = "".join(chars)

    # hash the password with the salt
    hashed_password = hash(password.join(salt))
    user_id = str(uuid4())
    # insert the user into the database
    conn = psycopg2.connect(
        database="test_database",
        host="0.0.0.0",
        port=5432,
        user="postgres",
        password="postgres",
    )
    print(conn)
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO "User" (id, username, email) VALUES (%s,%s,%s);',
        (user_id, username, email),
    )
    cursor.execute(
        'INSERT INTO "UserCredentials" (id, salt, password) VALUES (%s,%s,%s);',
        (user_id, salt, hashed_password),
    )
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
    if len(email) < 3 or len(email) > 320 or not re.fullmatch(regex, email):
        return False

    return True
