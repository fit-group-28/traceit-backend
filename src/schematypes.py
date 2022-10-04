from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from datetime import datetime

from typing import List


@dataclass
class Supplier(DataClassJsonMixin):
    supplier_id: int
    name: str


@dataclass
class Product(DataClassJsonMixin):
    product_id: int
    name: str
    supplier: Supplier


@dataclass
class ProductPayload(DataClassJsonMixin):
    product: Product
    quantity: int


def sumProductPayloads(
    payload1: ProductPayload | None, payload2: ProductPayload | None
) -> ProductPayload:
    """
    Sums two ProductPayloads.

    Args:
        payload1: The first ProductPayload.
        payload2: The second ProductPayload.

    Returns:
        The sum of the two ProductPayloads.
    """

    # a bit clunky to facilitate mypy type checking
    if payload2 is None:
        if payload1 is None:
            raise ValueError("Both payloads are None")
        else:
            return payload1
    else:
        if payload1 is None:
            return payload2
        if payload1.product.product_id == payload2.product.product_id:
            return ProductPayload(
                product=payload1.product,
                quantity=payload1.quantity + payload2.quantity,
            )

        else:
            raise ValueError(
                f"Product IDs do not match: {payload1.product.product_id} != {payload2.product.product_id}"
            )


@dataclass
class Order(DataClassJsonMixin):
    """
    A class representing the data of a response to an order request.

    Attributes:
        order_id: The order's ID.
        user_id: The user's ID.
        order_status: The order's status.
        date_placed: The date the order was placed.
        products: The products to order.
    """

    order_id: int
    user_id: int
    order_status: str
    date_placed: datetime
    products: List[ProductPayload]
