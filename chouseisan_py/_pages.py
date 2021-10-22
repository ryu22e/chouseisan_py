from __future__ import annotations

from bs4 import BeautifulSoup
from bs4.element import Tag
from requests.sessions import Session


class LoginError(Exception):
    pass


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

    def login(self, email: str, password: str) -> None:
        form_chousei_token = self.soup.find(id="form_chousei_token")
        chousei_token = (
            form_chousei_token.get("value")
            if isinstance(form_chousei_token, Tag)
            else ""
        )
        data = {
            "chousei_token": chousei_token,
            "email": email,
            "password": password,
            "remember": "1",
        }
        url = "https://chouseisan.com/auth/login"
        r = self.session.post(url, data=data)
        r.raise_for_status()
        self.soup = BeautifulSoup(r.content, "html.parser")
        if not self.is_authenticated:
            raise LoginError
