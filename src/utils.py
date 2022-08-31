from copy import deepcopy
from dataclasses_json import DataClassJsonMixin
from typing import Dict, Any


def copy_to_json(obj: DataClassJsonMixin) -> Dict[str, Any]:
    """
    Copy an object to a JSON-serializable dictionary."""
    return deepcopy(obj).to_dict()
