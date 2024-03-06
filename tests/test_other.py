from bot_app.user import User
from lib.backend_client import BackendClient


class TestUser:
    def setup_method(self):
        self.id = 1234
        self.tg_nick = 'username'

    def user(self):
        return User(tg_id=self.id, nick=self.tg_nick)

    def test_attrs(self):
        user = self.user()
        assert user.id == self.id
        assert user.nick == self.tg_nick

    def test_block(self):
        user = self.user()
        user.block()
        assert user.is_on_hold is True
        assert user.is_active is False

    def test_activate(self):
        user = self.user()
        user.block()
        user.activate()

        assert user.is_on_hold is False
        assert user.is_active is True


class TestBackendClient:
    def setup_method(self):
        self.client = BackendClient()

    def success_args(self, url):
        return {'url': url, 'status_code': 200, 'json': {"status": "success"}}

    def fail_args(self, url):
        return {'url': url, 'status_code': 500, 'text': '<p>Error, Sorry</p>'}

    def assert_success(self, response):
        assert response.is_successful is True
        assert response.status == 200
        assert response.request_url == self.url
        assert response.body == {"status": "success"}

    def test_get_current_tournaments(self, requests_mock):
        self.url = f"{BackendClient.URL}/tournaments/current"
        args = self.success_args(self.url)
        requests_mock.get(**args)
        self.assert_success(self.client.get_current_tournaments())

    def test_register(self, requests_mock):
        self.url = f"{BackendClient.URL}/tournaments/1/members/"
        args = self.success_args(self.url)
        requests_mock.post(**args)
        self.assert_success(self.client.register(user_id=1, user_name='name', current=1))

    def test_upload_file(self, requests_mock):
        self.url = f"{BackendClient.URL}/tournaments/1/members/1/prove_payment/"
        args = self.success_args(self.url)
        requests_mock.put(**args)
        self.assert_success(self.client.upload_file(1, 1, b'content'))

    def test_failed(self, requests_mock):
        url = f"{BackendClient.URL}/tournaments/current"
        args = self.fail_args(url)
        requests_mock.get(**args)
        response = self.client.get_current_tournaments()

        assert response.is_successful is False
        assert response.status == 500
        assert response.request_url == url
        assert 'error' in response.body
