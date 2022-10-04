from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from apidata import (
    ApiData,
    ApiResponse,
    jwt_failure,
    db_failure,
    JwtFailure,
    DbFailure,
    request_failure,
)
from userjwt import Jwt
from dbconnector import connQuery
from flask import Request
import datetime


@dataclass
class Supplier(DataClassJsonMixin):
    uid: str
    username: str
    number: int
    longitude: float
    latitude: float
    address: str
@dataclass
class Suppliers(DataClassJsonMixin):
    """
    A class representing the data of a response to a user details request.
    """
    suppliers: list[Supplier]



def endpoint_supplier_get(
    user_jwt: Jwt | None
) -> ApiResponse[Supplier | JwtFailure | DbFailure]:
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
        supplier = get_supplier()
        apiResponse = ApiResponse(
            response=Suppliers(suppliers=supplier),
            statusCode=200,
        )
    except Exception as e:
        return db_failure(e)

    return apiResponse


def get_supplier() -> list[Supplier]:
    """
    Get the supplier details for a user.
    """
    supplier = connQuery(
        [
            (
                'SELECT supplier_id, name, longitude, latitude, phone_number, address FROM "Supplier"',
            )
        ]
    )

    res = []
    if not supplier[0]:
        return None
    supplier = supplier[0]

    for row in supplier:
        supplierDist = {
            "supplier_id": row[0],
            "name": row[1],
            "longitude": row[2],
            "latitude": row[3],
            "phone_number": row[4],
            "address": row[5],
        }
        res.append(supplierDist)
    return res


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
