from telebot import TeleBot
from telebot.types import Message

from bot_app.ui_components import participant_keyboard, start_keyboard
from bot_app.user import User
from config.setup import lc
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
                lc('registration closed error'),
                reply_markup=start_keyboard()
            )

        if tournament.is_member(self.user.id):
            return self.bot.send_message(
                self.message.chat.id,
                lc('member status'),
                reply_markup=participant_keyboard()
            )

        self.bot.send_message(self.user.id, lc('viewer status'), reply_markup=start_keyboard())
