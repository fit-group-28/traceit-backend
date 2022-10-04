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
from schematypes import Order, ProductPayload, Product, Supplier

from typing import List, Dict

from flask import Request
import datetime


@dataclass
class Orders(DataClassJsonMixin):
    """
    A class representing the user's orders.

    Attributes:
        orders: The user's orders.
    """

    orders: List[Order]


def endpoint_order_get(
    user_jwt: Jwt | None,
) -> ApiResponse[ApiData[Orders] | JwtFailure | DbFailure]:
    """
    Handles the endpoint for fetching the user's orders.

    Args:
        user_jwt: The user's JWT.

    Returns:
        The user's orders.
    """

    if not user_jwt:
        return jwt_failure()

    try:
        orders = fetchOrdersQuery(user_jwt.username)
        return ApiResponse(
            response=ApiData(data=Orders(orders=orders)),
            statusCode=200,
        )

    except Exception as e:
        return db_failure(e)


def endpoint_order_patch(
    user_jwt: Jwt | None, request: Request
) -> ApiResponse[ApiData[Orders] | JwtFailure | DbFailure | RequestFailure]:
    """
    Handles the endpoint for updating the status of an order. Format is:

        {
            "order_id": 1,
            "order_status": "cancelled"
        }

    Returns:
        The updated order
    """
    if not user_jwt:
        return jwt_failure()

    requestJson = request.json

    # check body right format
    if (
        not isinstance(requestJson, dict)
        or not isinstance(requestJson.get("order_id", None), int)
        or (
            requestJson.get("order_status", None)
            not in ["placed", "transit", "fulfilled", "cancelled"]
        )
    ):
        return request_failure("Invalid request body")

    try:
        next(
            order
            for order in fetchOrdersQuery(user_jwt.username)
            if order.order_id == requestJson["order_id"]
        )

        updateOrderStatusQuery(requestJson["order_id"], requestJson["order_status"])

        updatedOrder = next(
            order
            for order in fetchOrdersQuery(user_jwt.username)
            if order.order_id == requestJson["order_id"]
        )

        return ApiResponse(
            response=ApiData(data=Orders(orders=[updatedOrder])),
            statusCode=200,
        )

    except StopIteration:
        return request_failure("User order not found")
    except Exception as e:
        return db_failure(e)


def endpoint_order_post(
    user_jwt: Jwt | None, request: Request
) -> ApiResponse[ApiData[Order] | JwtFailure | DbFailure | RequestFailure]:

    """
    Handles the endpoint for creating an order. Format is:

        {
            "products": [
                {
                    "product_id": 1,
                    "quantity": 1
                },
                {
                    "product_id": 2,
                    "quantity": 2
                }
            ]
        }

    Args:
        user_jwt: The user's JWT.
        request: The request object.

    Returns:
        The newly created order.

    """
    if not user_jwt:
        return jwt_failure()

    requestJson = request.json

    # check body right format
    if (
        not isinstance(requestJson, dict)
        or not isinstance(requestJson.get("products", None), list)
        or not requestJson.get("products", None)
    ) or not all(
        (
            isinstance(product, dict)
            and isinstance(product.get("product_id", None), int)
            and isinstance(product.get("quantity", None), int)
            and product.get("quantity", None) > 0
        )
        for product in requestJson["products"]
    ):
        return request_failure("Invalid request body")

    try:
        new_order_id = createOrderQuery(user_jwt.username, requestJson["products"])

        createdOrder = next(
            order
            for order in fetchOrdersQuery(user_jwt.username)
            if order.order_id == new_order_id
        )

        return ApiResponse(
            response=ApiData(data=Orders(orders=[createdOrder])),
            statusCode=200,
        )

    except Exception as e:
        return db_failure(e)


def createOrderQuery(username: str, prod_id_qty_pairs: List[Dict[str, int]]) -> int:
    """
    Performs the database query for creating an order.

    Returns:
        The newly created order.
    """

    with make_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                (
                    'INSERT INTO "Order" (user_id, order_status, date_placed) '
                    'VALUES ((SELECT id FROM "User" WHERE username = %s), %s, %s) '
                    "RETURNING order_id"
                ),
                (username, "placed", datetime.datetime.now()),
            )
            order_id = cursor.fetchone()[0]

            for prod_id_qty_pair in prod_id_qty_pairs:
                cursor.execute(
                    (
                        'INSERT INTO "Orderline" (order_id, product_id, quantity, subtotal) '
                        "VALUES (%s, %s, %s, %s)"
                    ),
                    (
                        order_id,
                        prod_id_qty_pair["product_id"],
                        prod_id_qty_pair["quantity"],
                        0,
                    ),
                )

    return order_id


def fetchOrdersQuery(username: str) -> List[Order]:
    """
    Performs the database query for user orders.

    Returns:
        The user's orders.
    """

    getOrdersQuery = [
        (
            (
                'SELECT "Order".order_id, "Orderline".product_id, "Product".name, "Supplier".name, "Supplier".supplier_id, quantity, user_id, order_status, date_placed '
                'FROM "Order" '
                'INNER JOIN "Orderline" ON "Orderline".order_id = "Order".order_id '
                'INNER JOIN "User" ON "User".id = "Order".user_id '
                'INNER JOIN "Product" ON "Orderline".product_id = "Product".product_id '
                'INNER JOIN "Supplier" ON "Product".supplier_id = "Supplier".supplier_id '
                "WHERE username = %s"
            ),
            (username,),
        )
    ]
    orders = connQuery(getOrdersQuery)

    orderDict = {}
    for orderLine in orders[0]:
        orderId = orderLine[0]
        if orderId not in orderDict:
            orderDict[orderId] = Order(
                order_id=orderId,
                user_id=orderLine[6].strip(),
                order_status=orderLine[7].strip(),
                date_placed=orderLine[8],
                products=[],
            )

        orderDict[orderId].products.append(
            ProductPayload(
                product=Product(
                    product_id=orderLine[1],
                    name=orderLine[2].strip(),
                    supplier=Supplier(
                        supplier_id=orderLine[4],
                        name=orderLine[3].strip(),
                    ),
                ),
                quantity=orderLine[5],
            )
        )

    return list(orderDict.values())


def updateOrderStatusQuery(order_id: int, order_status: str) -> None:
    """
    Updates the status of an order.

    Args:
        order_id: The id of the order.
        order_status: The new status of the order.
    """
    updateOrderQuery = [
        (
            ('UPDATE "Order" SET order_status = %s WHERE order_id = %s'),
            (order_status, order_id),
        )
    ]

    connExecute(updateOrderQuery)
