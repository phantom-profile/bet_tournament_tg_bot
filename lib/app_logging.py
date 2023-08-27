from datetime import datetime
from functools import wraps

import sentry_sdk
from telebot.types import Message


def logger_factory():
    def debug_request(f):
        @wraps(f)
        def inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if not isinstance(e, KeyboardInterrupt):
                    sentry_sdk.capture_exception(e)
                raise e

        return inner
    return debug_request


def log(message: Message):
    # TODO: Change to another log system (file logs mb)
    print("INFO:", datetime.now())
    print(f"Message from {message.from_user.first_name} {message.from_user.last_name}")
    print(f"(id = {message.from_user.id}) \n {message.text}")
    if message.document:
        print(f"File uploading {message.document.file_name}. ")
        print(f"File size: {message.document.file_size}")

