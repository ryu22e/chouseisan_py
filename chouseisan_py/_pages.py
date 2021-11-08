from __future__ import annotations

from urllib.parse import urljoin

from bs4 import BeautifulSoup
from bs4.element import Tag
from requests.sessions import Session

from .exceptions import LoginError, TagNotFoundError


class UserPage:
    def __init__(self, session: Session):
        self.session = session
        r = self.session.get("https://chouseisan.com/user")
        r.raise_for_status()
        self.soup = BeautifulSoup(r.content, "html.parser")

    @property
    def is_authenticated(self) -> bool:
        user_link = self.soup.select_one("a[href='/user']")
        return user_link is not None

    def login(self, email: str, password: str) -> None:
        attrs = {"id": "form_chousei_token"}
        form_chousei_token = self.soup.find(attrs=attrs)
        if not isinstance(form_chousei_token, Tag):
            raise TagNotFoundError(attrs)
        chousei_token = form_chousei_token.get("value")
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

    def go_to_top_page(self) -> TopPage:
        return TopPage(self.session)


class TopPage:
    def __init__(self, session: Session):
        self.session = session
        r = self.session.get("https://chouseisan.com/")
        r.raise_for_status()
        self.soup = BeautifulSoup(r.content, "html.parser")

    def _extract_action_url(self):
        attrs = {"id": "newEventForm"}
        new_event_form = self.soup.find(attrs=attrs)
        if not isinstance(new_event_form, Tag):
            raise TagNotFoundError(attrs)
        return new_event_form.get("action")

    def create_event(self, name: str, comment: str, kouho: str) -> NewEventPage:
        attrs = {"id": "chousei_token"}
        chousei_token = self.soup.find(attrs=attrs)
        if not isinstance(chousei_token, Tag):
            raise TagNotFoundError(attrs)
        chousei_token_value = chousei_token.get("value")
        data = {
            "chousei_token": chousei_token_value,
            "name": name,
            "comment": comment,
            "kouho": kouho,
        }
        action_url = self._extract_action_url()
        base_url = "https://chouseisan.com/schedule"
        url = urljoin(base_url, action_url)
        r = self.session.post(url, data)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        return NewEventPage(self.session, soup)


class NewEventPage:
    def __init__(self, session: Session, soup: BeautifulSoup):
        self.session = session
        self.soup = soup

    def get_event_url(self) -> str:
        attrs = {"id": "listUrl"}
        list_url = self.soup.find(attrs=attrs)
        if not isinstance(list_url, Tag):
            raise TagNotFoundError(attrs)
        value = list_url.get("value")
        if not value:
            value = ""
        return value[0] if isinstance(value, list) else value
