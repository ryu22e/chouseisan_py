"""Automates the operations of `調整さん <https://chouseisan.com/>`_ (Chouseisan)."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

import requests

from ._pages import UserPage


@dataclass(frozen=True)
class Auth:
    """Credentials for chouseisan.com."""

    email: str
    password: str


class Chouseisan:
    """Class to operate chouseisan.com."""

    _WEEKDAY_JP = ("月", "火", "水", "木", "金", "土", "日")

    def __init__(self, auth: Auth | None = None, cookies: dict | None = None):
        """Initialize the Chouseisan instance.

        :param auth: Credentials for chouseisan.com
        :param cookies: Cookies
        """
        self.auth = auth
        self.session = requests.session()
        if cookies:
            self.session.cookies.update(cookies)

    def _strftime(self, candidate: datetime) -> str:
        weekday_jp = self._WEEKDAY_JP[candidate.weekday()]
        return (
            f"{candidate.month}月{candidate.day}日({weekday_jp}) "
            f"{candidate.hour}:{candidate:%M}〜 "
        )

    def get_cookies(self) -> dict:
        """Get cookies.

        :returns: Cookies
        """
        return self.session.cookies.get_dict()

    def create_event(
        self,
        title: str,
        candidate_days: Iterable[datetime | str],
        comment: str = "",
    ) -> str:
        """Create event.

        :param title: Title of the event
        :param candidate_days: Candidate days for the event
        :param comment: Comment about the event
        :returns: Event URL
        :raises chouseisan_py.exceptions.LoginError: The login fails
        :raises chouseisan_py.exceptions.TagNotFoundError:
            The expected tag is not found in `調整さん <https://chouseisan.com/>`_
            (Chouseisan)
        :raises requests.HTTPError: An HTTP error occurred
        """
        user_page = UserPage(self.session)
        if self.auth and not user_page.is_authenticated:
            user_page.login(self.auth.email, self.auth.password)
        top_page = user_page.go_to_top_page()
        kouho_list = (
            self._strftime(candidate) if isinstance(candidate, datetime) else candidate
            for candidate in candidate_days
        )
        event = top_page.create_event(
            name=title, comment=comment, kouho="\n".join(kouho_list)
        )
        return event.get_event_url()
