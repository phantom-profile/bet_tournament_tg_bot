from telebot import TeleBot
from telebot.types import Message

from bot_app.message_sender import MessageSender
from bot_app.ui_components import participant_keyboard, start_keyboard
from bot_app.user import User
from lib.current_service import CurrentTournamentsService


class CheckStatusService:
    def __init__(self, user: User, message: Message, bot: TeleBot):
        self.user = user
        self.ui = MessageSender(bot, message.chat.id)

    def call(self):
        tournament = CurrentTournamentsService().call()
        if not tournament:
            return self.ui.send(message='registration closed error', keyboard=start_keyboard())

        if tournament.is_member(self.user.id):
            return self.ui.send(message='member status', keyboard=participant_keyboard())

        self.ui.send(message='viewer status', keyboard=start_keyboard())
