from telebot import TeleBot

from bot_app.ui_components import start_keyboard
from config.setup import lc


def initial_info(chat_id: int, bot: TeleBot):
    bot.send_message(chat_id, lc('start bot'), reply_markup=start_keyboard())


def rules_info(chat_id: int, bot: TeleBot):
    bot.send_message(chat_id, lc('membership rules'))
