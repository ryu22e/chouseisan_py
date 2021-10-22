from __future__ import annotations

from bs4 import BeautifulSoup
from requests.sessions import Session


class UserPage:
    def __init__(self, session: Session):
        self.session = session
        r = self.session.get("https://chouseisan.com/user")
        r.raise_for_status()
        self.soup = BeautifulSoup(r.content, "html.parser")

    @property
    def is_authenticated(self) -> bool:
        title = self.soup.title
        if not title:
            return False
        title_string = title.string
        return title_string.endswith("さんのマイページ | 調整さん") if title_string else False
