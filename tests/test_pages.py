from http import HTTPStatus

import pytest
import requests
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

    def test_raise_login_error_if_the_email_and_password_are_not_correct(
        self, html, responses
    ):
        """Raise login error if the email and password are not correct."""
        from chouseisan_py._pages import LoginError, UserPage

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
