from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from apidata import ApiData, ApiResponse, jwt_failure, db_failure, JwtFailure, DbFailure
from userjwt import Jwt
from dbconnector import connQuery
from ordertype import Order

from typing import List
from producttype import ProductPayload, Product
from ordertype import Order
from suppliertype import Supplier


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
    Returns a response to a hello world request.

    Returns:
        A response to the hello world request.
    """
    if not user_jwt:
        return jwt_failure()

    try:
        orders = ordersQuery(user_jwt.username)
        return ApiResponse(
            response=ApiData(data=Orders(orders=orders)),
            statusCode=200,
        )

    except Exception as e:
        return db_failure(e)


def ordersQuery(username: str) -> List[Order]:
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
            ("admin",),
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
