import telebot
from telebot.types import Message

from bot_app.ui_components import participant_keyboard, start_keyboard
from config import locale
from lib.backend_client import BackendClient


def check_status(message: Message, bot: telebot.TeleBot):
    print('chat id', message.chat.id)
    print('user id', message.from_user.id)
    client = BackendClient()
    if client.in_current_tournament(message.from_user.id):
        return bot.send_message(
            message.chat.id,
            locale.read('participant'),
            reply_markup=participant_keyboard()
        )

    bot.send_message(message.chat.id, locale.read('viewer'), reply_markup=start_keyboard())


def initial_info(chat_id: int, bot: telebot.TeleBot):
    bot.send_message(chat_id, locale.read('start'), reply_markup=start_keyboard())


def rules_info(chat_id: int, bot: telebot.TeleBot):
    bot.send_message(chat_id, locale.read('rules_faq'))
