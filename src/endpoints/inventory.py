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
from schematypes import Order, ProductPayload, Product, Supplier, sumProductPayloads

from typing import Iterable, List, Dict
from operator import eq, attrgetter
from functools import reduce
from funcy import compose, curry, partial

from flask import Request
import datetime
from endpoints.order import fetchOrdersQuery


@dataclass
class Inventory(DataClassJsonMixin):
    """
    Class representing the inventory of a product for a user.
    This is calculated from the sum of the fulfilled orders, the user's inventory offset and the user's consumed inventory from sales.

    Attributes:
        inventory: A list of products and their quantities.
    """

    inventory: List[ProductPayload]


def endpoint_inventory_get(
    user_jwt: Jwt | None,
) -> ApiResponse[ApiData[Inventory] | JwtFailure | DbFailure]:
    """
    Handles requests to get the user's current inventory.
    This is equal to the sum of the fulfilled orders, the user's base inventory offset (if present) and the user's consumed inventory from sales.

    Args:
        user_jwt: The user's JWT.

    Returns:
        The user's inventory.

    """
    if not user_jwt:
        return jwt_failure()

    try:
        inventory = getInventoryQuery(user_jwt.username)
        return ApiResponse(
            response=ApiData(data=Inventory(inventory=inventory)),
            statusCode=200,
        )

    except Exception as e:
        return db_failure(e)


def getInventoryQuery(username: str) -> List[ProductPayload]:
    """
    Gets the user's current inventory.
    This is equal to the sum of the fulfilled orders, the user's base inventory offset (if present) and the user's consumed inventory from sales.

    Args:
        username: The user's username.

    Returns:
        The user's inventory.

    """
    orders = fetchOrdersQuery(username)

    fulfilled_orders: Iterable[Order] = filter(
        compose(partial(eq, "fulfilled"), attrgetter("order_status")),
        orders,
    )
    fulfilled_order_payloads: Iterable[ProductPayload] = reduce(
        lambda acc, order: acc + order.products,
        fulfilled_orders,
        [],
    )

    offset_payloads = getProductOffsets(username)

    total_payloads: Dict[str, ProductPayload] = {}
    for payload in list(fulfilled_order_payloads) + offset_payloads:
        total_payloads[payload.product.product_id] = sumProductPayloads(
            payload, total_payloads.get(payload.product.product_id)
        )

    return [elem for elem in total_payloads.values() if elem.quantity > 0]


def getProductOffsets(
    username: str,
) -> List[ProductPayload]:
    """
    Gets the user's base inventory offset.

    Args:
        username: The user's username.

    Returns:
        The user's base inventory offset.
    """

    query = [
        (
            (
                'SELECT "UserProductOffset".product_id, "Product".name, "Supplier".supplier_id, "Supplier".name, quantity FROM "UserProductOffset" '
                'INNER JOIN "Product" ON "UserProductOffset".product_id = "Product".product_id '
                'INNER JOIN "Supplier" ON "Product".supplier_id = "Supplier".supplier_id '
                'WHERE user_id = (SELECT id FROM "User" WHERE username = %s)'
            ),
            (username,),
        )
    ]

    offsets = connQuery(query)

    return [
        ProductPayload(
            product=Product(
                product_id=offset[0],
                name=offset[1].strip(),
                supplier=Supplier(
                    supplier_id=offset[2],
                    name=offset[3].strip(),
                ),
            ),
            quantity=offset[4],
        )
        for offset in offsets[0]
    ]
