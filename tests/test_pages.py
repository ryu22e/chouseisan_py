import requests


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
            responses.GET, "https://chouseisan.com/user", body=html.read("login.html")
        )
        session = requests.session()

        p = UserPage(session)
        actual = p.is_authenticated

        assert actual is False
