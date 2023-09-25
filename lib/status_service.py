from telebot import TeleBot
from telebot.types import Message

from bot_app.ui_components import participant_keyboard, start_keyboard
from bot_app.user import User
from config.setup import locale
from lib.current_service import CurrentTournamentsService


class CheckStatusService:
    def __init__(self, user: User, message: Message, bot: TeleBot):
        self.user = user
        self.message = message
        self.bot = bot
        self._tournament = CurrentTournamentsService().call()['tournament']

    def call(self):
        tournament = CurrentTournamentsService().call()['tournament']
        if not tournament:
            return self.bot.send_message(
                self.message.chat.id,
                locale.read('registration_closed'),
                reply_markup=start_keyboard()
            )

        if tournament.is_member(self.user.id):
            return self.bot.send_message(
                self.message.chat.id,
                locale.read('already_participate'),
                reply_markup=participant_keyboard()
            )

        self.bot.send_message(self.user.id, locale.read('viewer'), reply_markup=start_keyboard())