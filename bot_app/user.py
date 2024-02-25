from telebot import types

from lib.base_client import Red


class User:
    def __init__(self, tg_user: types.User):
        self.id = tg_user.id
        self.nick = tg_user.username

    @property
    def is_on_hold(self) -> bool:
        return Red.conn.exists(self._lock_key)

    @property
    def is_active(self) -> bool:
        return not self.is_on_hold

    def block(self):
        Red.conn.set(self._lock_key, "true")

    def activate(self):
        Red.conn.delete(self._lock_key)

    @property
    def _lock_key(self):
        return f"lock-interface-{self.id}"
