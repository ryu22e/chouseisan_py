from datetime import datetime


class TestChouseisan:
    def test_create_event(self):
        from chouseisan_py import Auth, Chouseisan

        email = "test@example.com"
        password = "testpass"
        title = "test event"
        candidates = [
            datetime(2021, 10, 17, 19, 0),
            datetime(2021, 10, 18, 19, 0),
            datetime(2021, 10, 19, 20, 0),
            datetime(2021, 10, 20, 17, 0),
            "10/22(金) 19:00〜",
        ]
        comment = "This is test."

        auth = Auth(email, password)
        c = Chouseisan(auth)
        actual = c.create_event(title, candidates, comment)

        expected = "https://chouseisan.com/s?h=test"
        assert actual == expected
