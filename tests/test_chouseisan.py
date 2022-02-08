from datetime import datetime
from unittest.mock import MagicMock

import pytest
from requests import Session
from requests.cookies import RequestsCookieJar


@pytest.fixture()
def mock_user_page_instance(mocker):
    mock_user_page = mocker.patch("chouseisan_py.chouseisan.UserPage")
    mock_user_page_instance = mock_user_page.return_value
    mock_user_page_instance.is_authenticated = False

    return mock_user_page_instance


EVENT_URL = "https://chouseisan.com/s?h=test"


@pytest.fixture()
def mock_top_page_instance(mock_user_page_instance):
    mock_top_page_instance = mock_user_page_instance.go_to_top_page.return_value
    mock_new_event_page_instance = MagicMock()
    mock_new_event_page_instance.get_event_url.return_value = EVENT_URL
    mock_top_page_instance.create_event.return_value = mock_new_event_page_instance

    return mock_top_page_instance


class TestChouseisan:
    def test_create_event_returns_the_event_url(
        self, mock_top_page_instance, mock_user_page_instance
    ):
        """create_event returns the event URL."""
        from chouseisan_py.chouseisan import Auth, Chouseisan

        email = "test@example.com"
        password = "testpass"
        title = "test event"
        candidate_days = [
            datetime(2021, 10, 17, 19, 0),
            datetime(2021, 10, 18, 19, 0),
            datetime(2021, 10, 19, 20, 0),
            datetime(2021, 10, 20, 17, 0),
            "10/22(金) 19:00〜",
        ]
        comment = "This is test."

        auth = Auth(email, password)
        c = Chouseisan(auth)
        actual = c.create_event(title, candidate_days, comment)

        expected = EVENT_URL
        assert actual == expected
        mock_user_page_instance.login.assert_called_once_with(email, password)
        mock_top_page_instance.create_event.assert_called_once_with(
            name=title,
            comment=comment,
            kouho=(
                "10月17日(日) 19:00〜 \n"
                "10月18日(月) 19:00〜 \n"
                "10月19日(火) 20:00〜 \n"
                "10月20日(水) 17:00〜 \n"
                "10/22(金) 19:00〜"
            ),
        )

    def test_get_cookies(self, mocker):
        """Get cookies."""
        from chouseisan_py.chouseisan import Auth, Chouseisan

        mock_session_klass = MagicMock(wraps=Session)
        mocker.patch("requests.session", return_value=mock_session_klass)
        cookies = RequestsCookieJar()
        cookies["foo"] = "bar"
        mock_session_klass.cookies = cookies
        email = "test@example.com"
        password = "testpass"

        auth = Auth(email, password)
        c = Chouseisan(auth)
        actual = c.get_cookies()

        expected = dict(cookies)
        assert actual == expected

    def test_set_cookies_during_initialization(self):
        """Set cookies during initialization."""
        from chouseisan_py.chouseisan import Auth, Chouseisan

        email = "test@example.com"
        password = "testpass"
        cookies = {"foo": "bar"}

        auth = Auth(email, password)
        c = Chouseisan(auth, cookies)

        actual = c.session.cookies.get_dict()
        expected = cookies
        assert actual == expected
