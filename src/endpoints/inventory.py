from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from src.apidata import (
    ApiData,
    ApiResponse,
    RequestFailure,
    jwt_failure,
    db_failure,
    JwtFailure,
    DbFailure,
    request_failure,
)
from src.userjwt import Jwt
from src.dbconnector import connQuery, connExecute
from src.schematypes import Order, ProductPayload, Product, Supplier, sumProductPayloads

from typing import Iterable, List, Dict
from operator import eq, attrgetter
from functools import reduce
from funcy import compose, partial

from flask.wrappers import Request
from src.endpoints.order import fetchOrdersQuery


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


def endpoint_inventory_patch(
    user_jwt: Jwt | None,
    request: Request,
) -> ApiResponse[ApiData[Inventory] | JwtFailure | DbFailure | RequestFailure]:
    """
    Handles requests to update the user's current inventory. Updates the offset such that the new total inventory is equal to the target quantity.

    Format is:

        {
            "product_id": 123,
            "quantity": 10
        }

    Args:
        user_jwt: The user's JWT.
        request: The request object.

    Returns:
        The user's inventory.
    """
    if not user_jwt:
        return jwt_failure()

    requestJson = request.json

    # check body right format
    if (
        not isinstance(requestJson, dict)
        or not isinstance(requestJson.get("product_id", None), int)
        or not isinstance(requestJson.get("quantity", None), int)
        or requestJson["quantity"] < 0
    ):
        return request_failure("Invalid request body")

    try:
        inventory = updateInventoryQuery(
            user_jwt.username, requestJson["product_id"], requestJson["quantity"]
        )

        return ApiResponse(
            response=ApiData(data=Inventory(inventory=inventory)),
            statusCode=200,
        )

    except Exception as e:
        return db_failure(e)


def updateInventoryQuery(
    username: str, product_id: int, targetQuantity: int
) -> List[ProductPayload]:
    """
    Updates the user's current inventory.

    Args:
        username: The user's username.
        product_id: The product ID.
        quantity: The quantity of the product.

    Returns:
        The user's inventory.

    """
    inventory = getInventoryQuery(username)
    currentInvQuantity = (
        relevantProductPayload[0].quantity
        if (
            relevantProductPayload := list(
                filter(
                    lambda ppayload: ppayload.product.product_id == product_id,
                    inventory,
                )
            )
        )
        else 0
    )

    if targetQuantity != currentInvQuantity:
        offsets = getProductOffsets(username)
        currentOffsetQuantity = (
            relevantProductPayload[0].quantity
            if (
                relevantProductPayload := list(
                    filter(
                        lambda ppayload: ppayload.product.product_id == product_id,
                        offsets,
                    )
                )
            )
            else 0
        )

        newOffsetQuantity = currentOffsetQuantity + targetQuantity - currentInvQuantity

        query = [
            (
                (
                    'INSERT INTO "UserProductOffset" (user_id, product_id, quantity, subtotal) '
                    'VALUES ((SELECT id FROM "User" WHERE username = %s), %s, %s, %s) '
                    "ON CONFLICT (user_id, product_id) DO "
                    "UPDATE SET quantity = %s "
                    'WHERE "UserProductOffset".user_id = (SELECT id FROM "User" WHERE username = %s) '
                    'AND "UserProductOffset".product_id = %s'
                ),
                (
                    username,
                    product_id,
                    newOffsetQuantity,
                    0,
                    newOffsetQuantity,
                    username,
                    product_id,
                ),
            )
        ]

        connExecute(query)

    return getInventoryQuery(username)


def updateProductOffsetQuery(username: str, product_id: int, quantity: int) -> None:
    """
    Updates the user's base inventory offset.

    Args:
        username: The user's username.
        product_id: The product ID.
        quantity: The quantity of the product.

    Returns:
        None
    """

    query = [
        (
            (
                'UPDATE "UserProductOffset" SET quantity = %s WHERE user_id = (SELECT id FROM "User" WHERE username = %s) AND product_id = %s'
            ),
            (quantity, username, product_id),
        )
    ]

    connExecute(query)


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
    fulfilled_order_payloads: List[ProductPayload] = reduce(
        lambda acc, order: acc + order.products,
        fulfilled_orders,
        [],
    )

    offset_payloads = getProductOffsets(username)

    total_payloads: Dict[int, ProductPayload] = {}
    for payload in fulfilled_order_payloads + offset_payloads:
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
