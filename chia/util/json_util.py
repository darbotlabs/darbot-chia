from __future__ import annotations

import json
from typing import Any

from aiohttp import web


class EnhancedJSONEncoder(json.JSONEncoder):
    """
    Encodes bytes as hex strings with 0x, and converts all dataclasses to json.
    """

    def default(self, o: Any) -> Any:
        if hasattr(type(o), "to_json_dict"):
            return o.to_json_dict()
        elif hasattr(type(o), "__bytes__"):
            return f"0x{bytes(o).hex()}"
        elif isinstance(o, bytes):
            return f"0x{o.hex()}"
        return super().default(o)


def dict_to_json_str(o: Any) -> str:
    """
    Converts a python object into json.
    """
    try:
        json_str = json.dumps(o, cls=EnhancedJSONEncoder, sort_keys=True)
        return json_str
    except TypeError as e:
        # Sanitize error message to avoid exposing sensitive class names
        original_msg = str(e)
        if "is not JSON serializable" in original_msg:
            raise TypeError("Object is not JSON serializable") from e
        # For other TypeError messages, still sanitize but preserve more context
        raise TypeError("JSON serialization error") from e


def obj_to_response(o: Any) -> web.Response:
    """
    Converts a python object into json. Used for RPC server which returns JSON.
    """
    json_str = dict_to_json_str(o)
    return web.Response(body=json_str, content_type="application/json")
