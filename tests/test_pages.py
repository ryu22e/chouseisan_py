from http import HTTPStatus

import pytest
import requests
from bs4 import BeautifulSoup
from responses import matchers


class TestUserPage:
    def test_authenticated_if_the_title_tag_contains_the_user_page_title(
        self, html, responses
    ):
        """Should be authenticated, if the title tag contains the UserPage title."""
        from chouseisan_py._pages import UserPage

        responses.add(
            responses.GET, "https://chouseisan.com/user", body=html.read("user.html")
        )
        session = requests.session()

        p = UserPage(session)
        actual = p.is_authenticated

        assert actual is True

    def test_not_authenticated_if_the_title_tag_is_empty(self, html, responses):
        """Should not be authenticated, if the title tag is empty."""
        from chouseisan_py._pages import UserPage

        responses.add(
            responses.GET,
            "https://chouseisan.com/user",
            body="<html><body></body></html>",
        )
        session = requests.session()

        p = UserPage(session)
        actual = p.is_authenticated

        assert actual is False

    def test_not_authenticated_if_the_title_tag_does_not_contain_the_user_page_title(
        self, html, responses
    ):
        """Should not be authenticated, if the title tag does not contain the UserPage title."""
        from chouseisan_py._pages import UserPage

        responses.add(
            responses.GET,
            "https://chouseisan.com/user",
            body=html.read("login.html"),
            status=HTTPStatus.FOUND.value,
        )
        session = requests.session()

        p = UserPage(session)
        actual = p.is_authenticated

        assert actual is False

    def test_login_if_the_email_and_password_are_correct(self, html, responses):
        """Login if the email and password are correct."""
        from chouseisan_py._pages import UserPage

        responses.add(
            responses.GET,
            "https://chouseisan.com/user",
            body=html.read("login.html"),
            status=HTTPStatus.FOUND.value,
        )
        chousei_token = "testtoken"
        email = "test@example.com"
        password = "testpass"
        data = {
            "chousei_token": chousei_token,
            "email": email,
            "password": password,
            "remember": "1",
        }
        responses.add(
            responses.POST,
            "https://chouseisan.com/auth/login",
            body=html.read("user.html"),
            status=HTTPStatus.FOUND.value,
            match=[matchers.urlencoded_params_matcher(data)],
        )
        session = requests.session()

        p = UserPage(session)
        p.login(email, password)

    def test_raise_tag_not_found_error_if_token_is_not_found_at_login(
        self,
        responses,
    ):
        """Raise TagNotFoundError if token is not found at login."""
        from chouseisan_py._pages import UserPage
        from chouseisan_py.exceptions import TagNotFoundError

        responses.add(
            responses.GET,
            "https://chouseisan.com/user",
            body="<html><body></body></html>",
        )
        email = "test@example.com"
        password = "wrongpass"
        session = requests.session()

        p = UserPage(session)
        with pytest.raises(TagNotFoundError):
            p.login(email, password)

    def test_raise_login_error_if_the_email_and_password_are_not_correct(
        self, html, responses
    ):
        """Raise login error if the email and password are not correct."""
        from chouseisan_py._pages import UserPage
        from chouseisan_py.exceptions import LoginError

        responses.add(
            responses.GET,
            "https://chouseisan.com/user",
            body=html.read("login.html"),
            status=HTTPStatus.FOUND.value,
        )
        chousei_token = "testtoken"
        email = "test@example.com"
        password = "wrongpass"
        data = {
            "chousei_token": chousei_token,
            "email": email,
            "password": password,
            "remember": "1",
        }
        responses.add(
            responses.POST,
            "https://chouseisan.com/auth/login",
            body=html.read("login_error.html"),
            status=HTTPStatus.FOUND.value,
            match=[matchers.urlencoded_params_matcher(data)],
        )
        session = requests.session()

        p = UserPage(session)
        with pytest.raises(LoginError):
            p.login(email, password)

    def test_goto_top_page(self, html, responses):
        """Go to top page."""
        from chouseisan_py._pages import TopPage, UserPage

        responses.add(
            responses.GET, "https://chouseisan.com/user", body=html.read("user.html")
        )
        responses.add(
            responses.GET, "https://chouseisan.com/", body=html.read("top.html")
        )
        session = requests.session()

        p = UserPage(session)
        actual = p.go_to_top_page()

        assert type(actual) is TopPage

    def test_get_event_items(self, html, responses):
        """Get event list."""
        from chouseisan_py._pages import EventItem, UserPage

        responses.add(
            responses.GET, "https://chouseisan.com/user", body=html.read("user.html")
        )
        session = requests.session()

        p = UserPage(session)
        actual = p.get_event_items()

        expected = (
            EventItem(title="テストイベント1"),
            EventItem(title="テストイベント2"),
        )
        assert actual == expected


class TestTopPage:
    def test_show_top_page(self, html, responses):
        """Show top page."""
        from chouseisan_py._pages import TopPage

        responses.add(
            responses.GET, "https://chouseisan.com/", body=html.read("top.html")
        )
        session = requests.session()

        TopPage(session)

    def test_create_event(self, html, responses):
        """Create event."""
        from chouseisan_py._pages import NewEventPage, TopPage

        responses.add(
            responses.GET, "https://chouseisan.com/", body=html.read("top.html")
        )
        chousei_token = "testtoken"
        name = "テストイベント"
        comment = "テストコメント"
        kouho = """10/17(日) 19:00〜
10/18(月) 19:00〜
10/19(火) 19:00〜"""
        data = {
            "chousei_token": chousei_token,
            "name": name,
            "comment": comment,
            "kouho": kouho,
        }
        responses.add(
            responses.POST,
            "https://chouseisan.com/schedule/newEvent/create",
            body=html.read("new_event.html"),
            status=HTTPStatus.FOUND.value,
            match=[matchers.urlencoded_params_matcher(data)],
        )
        session = requests.session()

        p = TopPage(session)
        actual = p.create_event(name, comment, kouho)

        assert type(actual) is NewEventPage
        assert actual.get_event_url() == "https://chouseisan.com/s?h=test"

    def test_raise_tag_not_found_error_when_creating_an_event_if_action_url_is_not_found(
        self,
        html,
        responses,
    ):
        """Raise TagNotFoundError when creating event if action url is not found."""
        from chouseisan_py._pages import TopPage
        from chouseisan_py.exceptions import TagNotFoundError

        responses.add(
            responses.GET,
            "https://chouseisan.com/",
            body=r"""<html>
<body>
  <form>
    <input id="chousei_token" type="hidden" value="test">
  </form>
</body>
</html>""",
        )
        name = "テストイベント"
        comment = "テストコメント"
        kouho = """10/17(日) 19:00〜
10/18(月) 19:00〜
10/19(火) 19:00〜"""
        session = requests.session()

        p = TopPage(session)
        with pytest.raises(TagNotFoundError):
            p.create_event(name, comment, kouho)

    def test_raise_tag_not_found_error_when_creating_an_event_if_token_is_not_found(
        self,
        responses,
    ):
        """Raise TagNotFoundError when creating event if token is not found."""
        from chouseisan_py._pages import TopPage
        from chouseisan_py.exceptions import TagNotFoundError

        responses.add(
            responses.GET,
            "https://chouseisan.com/",
            body=r"""<html>
<body>
  <form id="newEventForm" action="test"></form>
</body>
</html>""",
        )
        name = "テストイベント"
        comment = "テストコメント"
        kouho = """10/17(日) 19:00〜
10/18(月) 19:00〜
10/19(火) 19:00〜"""
        session = requests.session()

        p = TopPage(session)
        with pytest.raises(TagNotFoundError):
            p.create_event(name, comment, kouho)


class TestNewEventPage:
    def test_get_event_url(self, html):
        """Get event url."""
        from chouseisan_py._pages import NewEventPage

        session = requests.session()
        new_event_url = "https://example.com/neweven"
        soup = BeautifulSoup(
            rf"""<html>
<body>
  <input id="listUrl" type="text" value="{new_event_url}">
</body>
</html>""",
            "html.parser",
        )

        new_event_page = NewEventPage(session, soup)
        actual = new_event_page.get_event_url()
        expected = new_event_url
        assert actual == expected

    def test_raise_tag_not_found_error_when_getting_event_url_if_list_url_text_is_not_found(
        self,
    ):
        """Raise TagNotFoundError when getting event url if list url text is not found."""
        from chouseisan_py._pages import NewEventPage
        from chouseisan_py.exceptions import TagNotFoundError

        session = requests.session()
        soup = BeautifulSoup("<html><body></body></html>", "html.parser")

        new_event_page = NewEventPage(session, soup)
        with pytest.raises(TagNotFoundError):
            new_event_page.get_event_url()
