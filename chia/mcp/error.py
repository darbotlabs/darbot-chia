from __future__ import annotations


class MCPError(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)

    def to_dict(self) -> dict[str, int | str]:
        return {"error": self.code, "message": self.message}
