from dataclasses import dataclass
from unicodedata import name
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
    """

    uid: str
    username: str
    number: int
    longitude: float
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
        print("-------------",supplier)
        apiResponse = ApiResponse(
            response=Supplier(uid=supplier["supplier_id"], username=supplier["name"], longitude=supplier["longitude"], latitude=supplier["latitude"], number=supplier["phone_number"]),
            statusCode=200,
        )
    except Exception as e:
        return db_failure(e)

    return apiResponse

def get_supplier(id: str) -> Supplier:
    """
    Get the supplier details for a user.
    """
    supplier = connQuery(
        [('SELECT supplier_id, name, longitude, latitude, phone_number FROM "Supplier" WHERE supplier_id = %s', (id,))]
    )

    if not supplier[0]:
        return None
    supplier = supplier[0][0]
    supplierDist = {}
    supplierDist = {"supplier_id": supplier[0], "name": supplier[1], "longitude": supplier[2], "latitude":supplier[3], "phone_number":supplier[4]}
    return supplierDist

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