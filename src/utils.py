from copy import deepcopy
from typing import Dict, Any
from dataclasses_json import DataClassJsonMixin


def copyToJson(obj: DataClassJsonMixin) -> Dict[str, Any]:
    """
    Copy an object to a JSON-serializable dictionary."""
    return deepcopy(obj).to_dict()
