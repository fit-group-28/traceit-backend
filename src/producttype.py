from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from suppliertype import Supplier


@dataclass
class Product(DataClassJsonMixin):
    product_id: int
    name: str
    supplier: Supplier


@dataclass
class ProductPayload(DataClassJsonMixin):
    product: Product
    quantity: int
