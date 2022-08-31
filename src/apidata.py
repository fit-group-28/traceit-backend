from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Dict, Any


@dataclass
class ApiData(DataClassJsonMixin):
    data: DataClassJsonMixin


def generate_api_json(obj: DataClassJsonMixin) -> Dict[str, Any]:
    """
    Generate an API JSON response from an object."""
    return ApiData(data=obj).to_dict()
