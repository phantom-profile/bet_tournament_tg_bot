from telebot import TeleBot

from bot_app.ui_components import participant_keyboard, start_keyboard
from bot_app.user import User
from config import locale


def check_status(user: User, bot: TeleBot):
    print('user id', user.id)
    if user.is_participant:
        return bot.send_message(
            user.id,
            locale.read('already_participate'),
            reply_markup=participant_keyboard()
        )

    bot.send_message(user.id, locale.read('viewer'), reply_markup=start_keyboard())


def initial_info(chat_id: int, bot: TeleBot):
    bot.send_message(chat_id, locale.read('start'), reply_markup=start_keyboard())


def rules_info(chat_id: int, bot: TeleBot):
    bot.send_message(chat_id, locale.read('rules_faq'))
