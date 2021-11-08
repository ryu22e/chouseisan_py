from __future__ import annotations

from typing import Any


class LoginError(Exception):
    # TODO Write docstring
    pass


class TagNotFoundError(Exception):
    # TODO Write docstring

    def __init__(self, attrs: dict[str, Any]):
        self._attrs = attrs

    def __str__(self):
        attrs = self._attrs
        return f"TagNotFoundError(attrs={attrs})"
