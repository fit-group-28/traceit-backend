from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class Supplier(DataClassJsonMixin):
    supplier_id: int
    name: str
