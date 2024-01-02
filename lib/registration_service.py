from telebot import TeleBot
from telebot.types import Message

from bot_app.message_sender import MessageSender
from bot_app.ui_components import (participant_keyboard,
                                   request_membership_keyboard, start_keyboard)
from bot_app.user import User
from lib.backend_client import BackendClient
from lib.current_service import CurrentTournamentsService

MB = 1 * 1024 * 1024


class RegisterOnTournamentService:
    def __init__(self, user: User, message: Message, bot: TeleBot):
        self.client = BackendClient()
        self.user = user
        self.message = message
        self.bot = bot
        self.ui = MessageSender(bot, chat_id=message.chat.id)

    def get_instructions(self):
        text, keyboard = self._init_reply_data()
        return self.ui.send(message=text, keyboard=keyboard)

    def hold_unlit_payment(self):
        if not self.tournament:
            return self.get_instructions()

        self.user.block()
        response = self.client.register(
            user_id=self.user.id,
            user_name=self.user.nick,
            current=self.tournament.id
        )
        if not response.is_successful:
            self.user.activate()
            return self.ui.send(message='default error')

        self.ui.send(message='payment request message')

    def pay(self):
        register_error = self._register_error()
        if register_error:
            return self.ui.send(message=register_error)

        file_info = self.bot.get_file(self.message.document.file_id)
        content = self.bot.download_file(file_info.file_path)
        response = self.client.upload_file(self.tournament.id, self.user.id, content)
        if response.is_successful:
            self.user.activate()
            self.ui.send(message='payment file sent', keyboard=participant_keyboard())
        else:
            return self.ui.send(message='default error')

    def _init_reply_data(self) -> tuple:
        if not self.tournament:
            return 'registration closed error', start_keyboard()

        if self.tournament.is_member(self.user.id):
            return 'member status', participant_keyboard()

        if self.tournament.is_full():
            return 'tournament is full error', start_keyboard()

        return 'register instruction', request_membership_keyboard()

    def _register_error(self):
        if not self.user.is_on_hold:
            return 'no file need error'

        if not self.message.document:
            return 'no file exists error'

        if self.message.document.file_size > MB:
            return 'file size limit error'

    @property
    def tournament(self):
        if not hasattr(self, '_tournament'):
            self._tournament = CurrentTournamentsService().call()

        return self._tournament
