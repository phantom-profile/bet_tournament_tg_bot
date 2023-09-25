import logging
from functools import wraps

import sentry_sdk
from telebot.types import Message


EXCLUDED_EXCEPTIONS = (KeyboardInterrupt,)


def logger_factory():
    def debug_request(f):
        @wraps(f)
        def inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if not isinstance(e, EXCLUDED_EXCEPTIONS):
                    sentry_sdk.capture_exception(e)
                    log_error(e)
                raise e

        return inner
    return debug_request


def log_tg_message(message: Message):
    log_message = "\n<----------------->\n" \
        f"message_sender: {message.from_user.first_name} {message.from_user.last_name} \n" \
        f"sender_id: {message.from_user.id} \n" \
        f"message_text: {message.text}\n"

    if message.document:
        log_message += f"file_name: {message.document.file_name}. \n" \
                       f"file_size: {message.document.file_size / 1024} KB\n"

    log_message += "<================>\n"
    logging.info(log_message)


def log_text(text: str, level=logging.WARNING, sentry=True, extra: dict = None):
    if sentry:
        sentry_sdk.capture_message(text, extra=extra or {})
    logging.log(level, text)


def log_error(error: Exception):
    logging.error(f"{error.__class__}", exc_info=True)
