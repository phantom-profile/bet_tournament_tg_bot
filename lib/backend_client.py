import requests

from config.setup import env_variables
from lib.base_client import BaseClient


class BackendClient(BaseClient):
    URL = f"{env_variables.get('BACKEND_URL')}/api/private"
    TOKEN = env_variables.get('BACKEND_TOKEN')

    def check_status(self, user_id: int, current: int):
        self._response = requests.get(
            url=self._build_url(f"tournaments/{current}/members/{user_id}/check"),
            params={"token": self.TOKEN}
        )

        return self._service_response

    def register(self, user_id: int, user_name: str, current: int):
        self._response = requests.post(
            url=self._build_url(f"tournaments/{current}/members/"),
            json={"tg_id": user_id, "tg_nickname": user_name},
            params={"token": self.TOKEN}
        )

        return self._service_response

    def get_current_tournaments(self):
        self._response = requests.get(
            url=self._build_url('tournaments/current'),
            params={"token": self.TOKEN}
        )

        return self._service_response

    def upload_file(self, tournament_id, user_id, file: bytes):
        self._response = requests.put(
            url=self._build_url(f'tournaments/{tournament_id}/members/{user_id}/prove_payment/'),
            params={"token": self.TOKEN},
            files={"payment_file": file}
        )

        return self._service_response
