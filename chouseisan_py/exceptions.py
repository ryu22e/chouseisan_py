from __future__ import annotations


class LoginError(Exception):
    # TODO Write docstring
    pass


class TagNotFoundError(Exception):
    # TODO Write docstring

    def __init__(self, selector: str):
        self._selector = selector

    def __str__(self):
        selector = self._selector
        return f"TagNotFoundError(selector={selector})"
