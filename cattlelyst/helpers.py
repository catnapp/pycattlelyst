from typing import Dict, List, Any
import hashlib
import json

# ref: https://www.doc.ic.ac.uk/~nuric/coding/how-to-hash-a-dictionary-in-python.html
def hash_dict(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


def hash_uuidable(
    uuidable: Dict[str, Any], ignore_keywords: List[str] = ["uuid"]
) -> str:
    if all([not k in uuidable for k in ignore_keywords]):
        return hash_dict(uuidable)

    else:  # `uuidable` needs to be sanitized of some ignored keywords
        uuidable_sanitized = uuidable.copy()

        for k in ignore_keywords:
            uuidable.pop(k, None)

        return hash_dict(uuidable_sanitized)


def hash_world_state(world_state: Dict[str, Any]) -> str:
    return hash_uuidable(
        world_state, ignore_keywords=["uuid", "next_state_uuid", "next_state_availablity_by_uuid"]
    )
