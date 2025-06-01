from __future__ import annotations

import pytest

from chia.util.json_util import dict_to_json_str, obj_to_response


class SensitiveClassNameExample:
    """A class with a potentially sensitive name that shouldn't be exposed in error messages."""

    def __init__(self) -> None:
        self.secret_key = "super_secret_key_12345"

    def __repr__(self) -> str:
        return f"SensitiveClassNameExample(secret_key={self.secret_key})"


def test_dict_to_json_str_does_not_expose_class_names() -> None:
    """Test that dict_to_json_str doesn't expose sensitive class names in exception messages."""

    # Create an object that can't be JSON serialized
    non_serializable_obj = SensitiveClassNameExample()

    # Test that the exception message doesn't contain the class name
    with pytest.raises(TypeError) as exc_info:
        dict_to_json_str({"data": non_serializable_obj})

    error_message = str(exc_info.value)

    # The error message should not contain the class name "SensitiveClassNameExample"
    assert "SensitiveClassNameExample" not in error_message, f"Class name exposed in error: {error_message}"

    # It should be a generic error message
    assert error_message == "Object is not JSON serializable", f"Unexpected error message: {error_message}"


def test_obj_to_response_does_not_expose_class_names() -> None:
    """Test that obj_to_response doesn't expose sensitive class names in exception messages."""

    # Create an object that can't be JSON serialized
    non_serializable_obj = SensitiveClassNameExample()

    # Test that the exception message doesn't contain the class name
    with pytest.raises(TypeError) as exc_info:
        obj_to_response({"data": non_serializable_obj})

    error_message = str(exc_info.value)

    # The error message should not contain the class name "SensitiveClassNameExample"
    assert "SensitiveClassNameExample" not in error_message, f"Class name exposed in error: {error_message}"

    # It should be a generic error message
    assert error_message == "Object is not JSON serializable", f"Unexpected error message: {error_message}"


def test_json_util_handles_normal_objects() -> None:
    """Test that normal JSON serializable objects still work correctly."""

    # Test with normal serializable objects
    test_data = {
        "string": "test",
        "number": 42,
        "boolean": True,
        "array": [1, 2, 3],
        "null": None,
        "nested": {"key": "value"}
    }

    # Should work normally
    json_str = dict_to_json_str(test_data)
    assert isinstance(json_str, str)
    assert "test" in json_str

    # obj_to_response should also work
    response = obj_to_response(test_data)
    assert response.content_type == "application/json"
