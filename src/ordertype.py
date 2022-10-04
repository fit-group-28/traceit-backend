from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from datetime import datetime

from typing import List
from producttype import ProductPayload


@dataclass
class Order(DataClassJsonMixin):
    order_id: int
    user_id: int
    order_status: str
    date_placed: datetime
    products: List[ProductPayload]
