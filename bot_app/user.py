from telebot import types

from lib.base_client import Red


class User:
    def __init__(self, tg_user: types.User):
        self.id = tg_user.id
        self.nick = tg_user.username

    @property
    def is_on_hold(self) -> bool:
        return Red.exists(self._lock_key)

    def block(self):
        Red.set(self._lock_key, "true")

    def activate(self):
        Red.delete(self._lock_key)

    @property
    def _lock_key(self):
        return f"lock-interface-{self.id}"
