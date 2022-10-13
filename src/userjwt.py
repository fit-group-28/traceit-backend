from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


from flask_jwt_extended import get_jwt_identity


@dataclass
class Jwt(DataClassJsonMixin):
    """
    A class representing a JSON Web Token."""

    username: str
    time_issued: int


def get_user_jwt() -> Jwt | None:
    """
    Get the user's JWT.

    Returns:
        The user's JWT if it exists, None otherwise.
    """
    try:
        return (
            Jwt.from_dict(user_identity)
            if (user_identity := get_jwt_identity())
            else None
        )
    except Exception:
        return None
