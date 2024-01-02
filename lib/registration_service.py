from telebot import TeleBot
from telebot.types import Message

from bot_app.ui_components import (participant_keyboard,
                                   request_membership_keyboard, start_keyboard)
from bot_app.user import User
from config.setup import lc
from lib.backend_client import BackendClient
from lib.current_service import CurrentTournamentsService

MB = 1 * 1024 * 1024


class RegisterOnTournamentService:
    def __init__(self, user: User, message: Message, bot: TeleBot):
        self.client = BackendClient()
        self.user = user
        self.message = message
        self.bot = bot
        self._tournament = None

    def get_instructions(self):
        text, keyboard = self._init_reply_data()
        return self.bot.send_message(
            chat_id=self.message.chat.id,
            text=text,
            reply_markup=keyboard
        )

    def hold_unlit_payment(self):
        if not self.tournament:
            return self.get_instructions()

        self.user.block()
        response = self.client.register(
            user_id=self.user.id,
            user_name=self.user.nick,
            current=self.tournament.id
        )
        if not response['is_successful']:
            self.user.activate()
            return self.bot.send_message(chat_id=self.message.chat.id, text=lc("default error"))

        self.bot.send_message(
            chat_id=self.message.chat.id,
            text=lc('payment request message')
        )

    def pay(self):
        register_error = self._register_error()
        if register_error:
            return self.bot.send_message(
                chat_id=self.message.chat.id,
                text=register_error
            )

        file_info = self.bot.get_file(self.message.document.file_id)
        content = self.bot.download_file(file_info.file_path)
        response = self.client.upload_file(self.tournament.id, self.user.id, content)
        if response['is_successful']:
            self.user.activate()
            self.bot.send_message(
                chat_id=self.message.chat.id,
                text=lc('payment file sent'),
                reply_markup=participant_keyboard()
            )
        else:
            return self.bot.send_message(chat_id=self.message.chat.id, text=lc("default error"))

    def _init_reply_data(self) -> tuple:
        if not self.tournament:
            return lc('registration closed error'), start_keyboard()

        if self.tournament.is_member(self.user.id):
            return lc('member status'), participant_keyboard()

        if self.tournament.is_full():
            return lc('tournament is full error'), start_keyboard()

        return lc('register instruction'), request_membership_keyboard()

    def _register_error(self):
        if not self.user.is_on_hold:
            return lc('no file need error')

        if not self.message.document:
            return lc('no file exists error')

        if self.message.document.file_size > MB:
            return lc('file size limit error')

    @property
    def tournament(self):
        if not self._tournament:
            self._tournament = CurrentTournamentsService().call()['tournament']

        return self._tournament
