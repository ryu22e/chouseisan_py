from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Auth:
    """Credentials for chouseisan.com."""

    email: str
    password: str
    storage_state_path: Path | str | None = None


class Chouseisan:
    """Class to operate chouseisan.com."""

    def __init__(self, auth: Auth | None = None):
        # TODO Write docstring
        self.auth = auth

    def create_event(
        self,
        title: str,
        candidates: Iterable[datetime | str],
        comment: str = "",
        *,
        omit_year: bool = True,
    ) -> str:
        # TODO Write docstring
        # TODO Write the production code
        expected = "https://chouseisan.com/s?h=test"
        return expected
