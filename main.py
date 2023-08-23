from dataclasses import dataclass, field
from time import sleep

from flask import Flask, request
from bot import bot, env_variables


app = Flask(__name__)


@dataclass
class SendParams:
    chat_ids: list[int]
    message: str
    errors: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.chat_ids, list):
            self.errors.append("chat_ids param required as list of ids")
        if not isinstance(self.message, str):
            self.errors.append("message param required as formatted string")

    def as_dict(self):
        return {"chat_ids": self.chat_ids, "message": self.message}


@app.route("/tgsend", methods=['POST'])
def hello_world():
    if request.args.get('token') != env_variables.get('API_ACCESS_TOKEN'):
        return {"errors": ["Invalid access token"]}, 403
    params = SendParams(
        chat_ids=request.json.get('chat_ids'),
        message=request.json.get('message')
    )
    if params.errors:
        return {"errors": params.errors}, 422

    for chat_id in params.chat_ids:
        bot.send_message(chat_id, f"{params.message}")
        sleep(0.3)

    return params.as_dict()
