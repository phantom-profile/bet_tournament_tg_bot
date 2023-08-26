from lib.backend_client import BackendClient
from lib.base_client import Red


class User:
    def __init__(self, user_id: int):
        self.id = user_id
        self.client = BackendClient()

    @property
    def is_temp_blocked(self) -> bool:
        return Red.exists(self._lock_key)

    def block(self):
        Red.set(self._lock_key, "true")

    @property
    def is_participant(self) -> bool:
        return self.client.in_current_tournament(self.id)

    @property
    def _lock_key(self):
        return f"lock-interface-{self.id}"
