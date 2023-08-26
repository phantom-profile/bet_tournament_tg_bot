from telebot import TeleBot

from bot_app.ui_components import participant_keyboard, start_keyboard
from config import locale
from lib.backend_client import BackendClient


def check_status(user_id: int, bot: TeleBot):
    print('user id', user_id)
    client = BackendClient()
    if client.in_current_tournament(user_id):
        return bot.send_message(
            user_id,
            locale.read('participant'),
            reply_markup=participant_keyboard()
        )

    bot.send_message(user_id, locale.read('viewer'), reply_markup=start_keyboard())


def initial_info(chat_id: int, bot: TeleBot):
    bot.send_message(chat_id, locale.read('start'), reply_markup=start_keyboard())


def rules_info(chat_id: int, bot: TeleBot):
    bot.send_message(chat_id, locale.read('rules_faq'))
