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
from schematypes import Order, ProductExtended, ProductPayload, Product, Supplier

from typing import List, Dict

from flask import Request
import datetime


@dataclass
class Products(DataClassJsonMixin):
    """
    A class representing the user's orders.

    Attributes:
        orders: The user's orders.
    """

    products: List[ProductExtended]


def endpoint_product_get() -> ApiResponse[ApiData[Products] | DbFailure]:

    try:
        products = fetchProductsQuery()
        return ApiResponse(
            response=ApiData(data=Products(products=products)),
            statusCode=200,
        )

    except Exception as e:
        return db_failure(e)


def fetchProductsQuery() -> List[ProductExtended]:
    """
    Performs the database query for user orders.

    Returns:
        The user's orders.
    """

    getProductsQuery = [
        (
            (
                'SELECT product_id, "Product".name, price, description, "Supplier".name, "Supplier".supplier_id '
                'FROM "Product" '
                'INNER JOIN "Supplier" ON "Product".supplier_id = "Supplier".supplier_id '
            ),
            (),
        )
    ]
    products = connQuery(getProductsQuery)

    productList = []

    for productTuple in products[0]:
        product = ProductExtended(
            product_id=productTuple[0],
            name=productTuple[1].strip(),
            price=str(productTuple[2]).strip(),
            description=productTuple[3].strip(),
            supplier=Supplier(name=productTuple[4], supplier_id=productTuple[5]),
        )
        productList.append(product)

    return productList
