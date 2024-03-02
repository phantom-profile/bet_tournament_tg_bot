from dataclasses import dataclass, field
from time import sleep

from flask import Flask, request

from bot_app.message_sender import MessageSender
from config.setup import env_variables
from event_handlers import bot

app = Flask(__name__)


@dataclass
class SendMessagesService:
    chat_ids: list[int]
    message: str
    token: str
    errors: list[str] = field(default_factory=list)
    response: dict = None
    status: int = None

    def __post_init__(self):
        if self.token != env_variables.get('API_ACCESS_TOKEN'):
            self.errors.append('Invalid access token')
            return
        if not isinstance(self.chat_ids, list):
            self.errors.append('chat_ids param required as list of ids')
        if not isinstance(self.message, str):
            self.errors.append('message param required as formatted string')

    def call(self):
        if self.errors:
            self.response, self.status = {'errors': self.errors}, 400
            return
        for chat_id in self.chat_ids:
            MessageSender(bot, chat_id).send_raw(self.message)
            sleep(0.2)
        self.response = {'chat_ids': self.chat_ids, 'message': self.message}
        self.status = 200


@app.route('/tgsend', methods=['POST'])
def send_message():
    service = SendMessagesService(
        chat_ids=request.json.get('chat_ids'),
        message=request.json.get('message'),
        token=request.args.get('token')
    )
    service.call()
    return service.response, service.status
