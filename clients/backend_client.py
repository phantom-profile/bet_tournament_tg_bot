from config import env_variables
from clients.base_client import BaseClient


class BackendClient(BaseClient):
    URL = env_variables.get('BACKEND_URL')
    TOKEN = env_variables.get('BACKEND_TOKEN')

    def in_current_tournament(self, user_id) -> bool:
        return True
