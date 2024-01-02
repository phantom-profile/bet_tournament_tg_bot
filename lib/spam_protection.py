from functools import wraps

from telebot import TeleBot
from telebot.types import Message

from lib.base_client import Red
from bot_app.message_sender import MessageSender


class SpamProtector:
    PREFIX = 'user::requests-count'
    LIMIT = 5
    SECONDS = 30

    ALLOW = 1
    WARN = 2
    FORBID = 3

    __slots__ = ('user_id',)

    def __init__(self, user_id: int):
        self.user_id = user_id

    def decision(self) -> int:
        key = f'{self.PREFIX}::{self.user_id}'
        count = Red.incr(key)
        if count == 1:
            Red.expire(key, self.SECONDS)
        if count > self.LIMIT:
            return self.FORBID
        if count < self.LIMIT:
            return self.ALLOW
        if count == self.LIMIT:
            return self.WARN


def control_rate_limit(tg_bot: TeleBot):
    def decorator(f):
        @wraps(f)
        def wrapper(message: Message, *args, **kwargs):
            user_id = message.from_user.id
            result = SpamProtector(user_id).decision()
            if result == SpamProtector.FORBID:
                return
            if result == SpamProtector.ALLOW:
                return f(message, *args, **kwargs)
            if result == SpamProtector.WARN:
                return MessageSender(tg_bot, user_id).send('rate limit error')
        return wrapper
    return decorator
