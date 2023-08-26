from config import env_variables
from lib.base_client import BaseClient, Red


class BackendClient(BaseClient):
    URL = env_variables.get('BACKEND_URL')
    TOKEN = env_variables.get('BACKEND_TOKEN')
    FIVE_MINUTES = 5 * 60  # for test. Later it is gonna be api request

    def in_current_tournament(self, user_id: int) -> bool:
        return Red.exists(f"tournament_participant-{user_id}")

    def register(self, user_id: int):
        Red.setex(f"tournament_participant-{user_id}", self.FIVE_MINUTES, "true")

    def is_registration_opened(self) -> bool:
        return len(Red.keys("tournament_participant*")) < 1
