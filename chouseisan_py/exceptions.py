"""Errors that occurs during
 `調整さん <https://chouseisan.com/>`_ (Chouseisan) operation."""
from __future__ import annotations


class LoginError(Exception):
    """Error that occurs when login fails."""

    pass


class TagNotFoundError(Exception):
    """Error that occurs when the expected HTML tag
    does not exist on `調整さん <https://chouseisan.com/>`_ (Chouseisan)."""

    def __init__(self, selector: str):
        """Initialize the Chouseisan instance.

        :param selector: The specified selector
        """
        self._selector = selector

    def __str__(self):
        selector = self._selector
        return f"TagNotFoundError(selector={selector})"
