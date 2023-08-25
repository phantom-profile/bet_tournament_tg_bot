import random

from config import env_variables
from lib.base_client import BaseClient


class BackendClient(BaseClient):
    URL = env_variables.get('BACKEND_URL')
    TOKEN = env_variables.get('BACKEND_TOKEN')

    def in_current_tournament(self, user_id) -> bool:
        return random.choice([True, False])
