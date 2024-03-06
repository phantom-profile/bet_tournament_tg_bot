from os import getenv

import requests

from lib.base_client import BaseClient


class BackendClient(BaseClient):
    URL = f"{getenv('BACKEND_URL')}/api/private"
    TOKEN = getenv('BACKEND_TOKEN')
    AUTH = {"Authorization": f"Token {TOKEN}"}

    def register(self, user_id: int, user_name: str, current: int):
        self._response = requests.post(
            url=self._build_url(f"tournaments/{current}/members/"),
            json={"tg_id": user_id, "tg_nickname": user_name},
            headers=self.AUTH
        )

        return self._service_response

    def get_current_tournaments(self):
        self._response = requests.get(
            url=self._build_url('tournaments/current'),
            headers=self.AUTH
        )

        return self._service_response

    def upload_file(self, tournament_id, user_id, file: bytes):
        self._response = requests.put(
            url=self._build_url(f'tournaments/{tournament_id}/members/{user_id}/prove_payment/'),
            files={"payment_file": file},
            headers=self.AUTH
        )

        return self._service_response
