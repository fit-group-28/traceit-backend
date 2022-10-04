from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from datetime import datetime

from typing import List, Dict
from producttype import ProductPayload


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
