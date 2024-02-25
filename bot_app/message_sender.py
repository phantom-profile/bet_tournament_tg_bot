from typing import Protocol

from config.setup import lc


class SendInterface(Protocol):
    def send_message(self, text: str, chat_id: str, reply_markup=None):
        ...


class MessageSender:
    def __init__(self, sender: SendInterface, chat_id):
        self.sender = sender
        self.chat_id = chat_id

    def send(self, message, keyboard=None):
        self.sender.send_message(text=lc(message), chat_id=self.chat_id, reply_markup=keyboard)
