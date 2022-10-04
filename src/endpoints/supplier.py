from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from apidata import (
    ApiData,
    ApiResponse,
    RequestFailure,
    jwt_failure,
    db_failure,
    JwtFailure,
    DbFailure,
    request_failure,
)
from userjwt import Jwt
from dbconnector import connQuery, make_connection, connExecute
from suppliertype import Supplier

from typing import List, Dict
from producttype import ProductPayload, Product
from ordertype import Order
from suppliertype import Supplier

from flask import Request
import datetime


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
    number: int
    longtitude: float
    latitude: float

def endpoint_supplier_get(user_jwt: Jwt | None, request: Request) -> ApiResponse[Supplier| JwtFailure | DbFailure]:
    """
    Handles the endpoint for getting supplier details.

        Args:
            user_jwt: The user's JWT.

        Returns:
            A response to the get supplier details request.
    """
    if not user_jwt:
        return jwt_failure()

    try:
        requestJson = request.get_json()
        supplier = get_supplier(requestJson.get("supplier_id", None))
        apiResponse = ApiResponse(
            response=Supplier(
                msg="Supplier details retrieved",
                supplier_id=supplier.supplier_id,
                name=supplier.name,
                longitude=supplier.longitude,
                latitude=supplier.latitude,
                number=supplier.phone_number
            ),
            statusCode=200,
        )
    except Exception as e:
        return db_failure(e)

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
        longitude=supplier.longitude,
        latitude=supplier.latitude,
        number=supplier.phone_number,
    )

def endpoint_supplier_product_get(user_jwt: Jwt | None) -> ApiResponse[Supplier]:
    """
    Handles the endpoint for getting supplier product details.

        Args:
            user_jwt: The user's JWT.

        Returns:
            A response to the get supplier product details request.
    """
    if not user_jwt:
        return jwt_failure()
    
    try:
        supplier = get_supplier_product(user_jwt.user_id)
        apiResponse = ApiResponse(
            response=Supplier(
                msg="Supplier product details retrieved",
                supplier_id=supplier.supplier_id,
                name=supplier.name,
                longitude=supplier.longitude,
                latitude=supplier.latitude,
                number=supplier.phone_number,
            ),
            statusCode=200,
        )
    except Exception as e:
        return db_failure(e)


    return apiResponse

def get_supplier_product(user_id: str) -> Supplier:
    """
    Get the supplier product details for a user.
    """
    supplier = connQuery(
        "SELECT * FROM product WHERE supplier_id = %s", (user_id,)
    ).fetchone()
    return Supplier(
        supplier_id=supplier.supplier_id,
        name=supplier.name,
    )

def __fetchSupplierQuery(username: str) -> Supplier:
    """
    Fetches the user's orders from the database.

    Args:
        username: The username of the user.

    Returns:
        The user's orders.
    """
    query = """
        SELECT * FROM supplier WHERE supplier_id = %s
    """
    return connQuery(query, (username,)).fetchone()