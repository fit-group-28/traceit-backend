from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from apidata import ApiData, ApiResponse, JwtFailure, DbFailure, jwt_failure, db_failure
from userjwt import Jwt
from dbconnector import connQuery

from typing import Tuple

@dataclass
class Supplier(DataClassJsonMixin):
    """
    A class representing the data of a response to a user details request.

    Attributes:
        username: The username of the user.
        time_issued: The time the user's token was issued.
        email: The email of the user.
    """

    uid: str
    username: str

def endpoint_supplier_get(user_jwt: Jwt | None) -> ApiResponse[Supplier]:
    """
    Handles the endpoint for getting supplier details.

        Args:
            user_jwt: The user's JWT.

        Returns:
            A response to the get supplier details request.
    """
    if user_jwt is None:
        apiResponse = ApiResponse(
            response=Supplier(msg="User not logged in"), statusCode=401
        )
    else:
        try:
            supplier = get_supplier(user_jwt.user_id)
            apiResponse = ApiResponse(
                response=Supplier(
                    msg="Supplier details retrieved",
                    supplier_id=supplier.supplier_id,
                    name=supplier.name,
                ),
                statusCode=200,
            )
        except Exception:
            apiResponse = ApiResponse(
                response=Supplier(msg="Supplier details retrieval failure"),
                statusCode=401,
            )

    return apiResponse

def get_supplier(user_id: str) -> Supplier:
    """
    Get the supplier details for a user.
    """
    supplier = connQuery(
        "SELECT * FROM supplier WHERE user_id = %s", (user_id,)
    ).fetchone()
    return Supplier(
        supplier_id=supplier.supplier_id,
        name=supplier.name,
    )

def endpoint_supplier_product_get(user_jwt: Jwt | None) -> ApiResponse[Supplier]:
    """
    Handles the endpoint for getting supplier product details.

        Args:
            user_jwt: The user's JWT.

        Returns:
            A response to the get supplier product details request.
    """
    if user_jwt is None:
        apiResponse = ApiResponse(
            response=Supplier(msg="User not logged in"), statusCode=401
        )
    else:
        try:
            supplier = get_supplier_product(user_jwt.user_id)
            apiResponse = ApiResponse(
                response=Supplier(
                    msg="Supplier product details retrieved",
                    supplier_id=supplier.supplier_id,
                    name=supplier.name,
                ),
                statusCode=200,
            )
        except Exception:
            apiResponse = ApiResponse(
                response=Supplier(msg="Supplier product details retrieval failure"),
                statusCode=401,
            )

    return apiResponse

def get_supplier_product(user_id: str) -> Supplier:
    """
    Get the supplier product details for a user.
    """
    supplier = connQuery(
        "SELECT * FROM product WHERE user_id = %s", (user_id,)
    ).fetchone()
    return Supplier(
        supplier_id=supplier.supplier_id,
        name=supplier.name,
    )