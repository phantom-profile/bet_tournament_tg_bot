from pathlib import Path

import telebot
from telebot import types
from telebot.types import Message

from config import env_variables
from lib.base_client import Red
from lib.locale_service import LocaleService
from lib.backend_client import BackendClient


bot = telebot.TeleBot(env_variables.get('TG_BOT_TOKEN'), parse_mode=None)
locale = LocaleService()

MB = 1 * 1024 * 1024

def init_payment_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    payment = types.InlineKeyboardButton(text=locale.read('request_pay_proof'))
    keyboard.add(payment)
    return keyboard


def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rules = types.KeyboardButton(text=locale.read('rules'))
    register = types.KeyboardButton(text=locale.read('register'))
    status = types.KeyboardButton(text=locale.read('status'))
    keyboard.add(rules, register, status)
    return keyboard


def participant_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    make_bet = types.KeyboardButton(text=locale.read('make_bet'))
    rules = types.KeyboardButton(text=locale.read('rules'))
    status = types.KeyboardButton(text=locale.read('status'))
    keyboard.add(make_bet, rules, status)
    return keyboard


def check_status(message: Message):
    print(message.chat.id)
    print(message.from_user.id)
    client = BackendClient()
    if client.in_current_tournament(message.from_user.id):
        return bot.send_message(
            message.chat.id,
            locale.read('participant'),
            reply_markup=participant_keyboard()
        )

    bot.send_message(message.chat.id, locale.read('viewer'), reply_markup=start_keyboard())


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    print(message.chat.id)
    bot.send_message(message.chat.id, locale.read('start'), reply_markup=start_keyboard())


@bot.message_handler(content_types=['text'])
def message_reply(message: Message):
    print(message.text)
    if Red.exists(f"lock-interface-{message.from_user.id}"):
        bot.send_message(message.chat.id, locale.read('pay_proof_message'))
        return

    if message.text == locale.read('rules'):
        bot.send_message(message.chat.id, locale.read('rules_faq'))
    elif message.text == locale.read('register'):
        client = BackendClient()
        if not client.is_registration_opened():
            return bot.send_message(
                message.chat.id,
                locale.read('registration_closed'),
                reply_markup=participant_keyboard()
            )
        if client.in_current_tournament(message.from_user.id):
            return bot.send_message(
                message.chat.id,
                locale.read('already_participate'),
                reply_markup=participant_keyboard()
            )
        bot.send_message(message.chat.id, locale.read('register_instruction'), reply_markup=init_payment_keyboard())
    elif message.text == locale.read('status'):
        check_status(message)
    elif message.text == locale.read('request_pay_proof'):
        bot.send_message(message.chat.id, locale.read('pay_proof_message'))
        Red.set(f"lock-interface-{message.from_user.id}", "true")


@bot.message_handler(content_types=['document'])
def get_payment_proof(message: Message):
    client = BackendClient()

    if not Red.exists(f"lock-interface-{message.from_user.id}") or client.in_current_tournament(message.from_user.id):
        bot.send_message(message.chat.id, locale.read('no_file_need'))
        return

    if not message.document:
        return

    if message.document.file_size > MB:
        bot.send_message(message.chat.id, locale.read('file_size_limit'))
        return

    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    new_file = Path('uploaded', file_name)
    with new_file.open('wb') as file:
        file.write(downloaded_file)

    bot.send_message(message.chat.id, locale.read('proof_sent'), reply_markup=participant_keyboard())
    Red.delete(f"lock-interface-{message.from_user.id}")
    client.register(message.from_user.id)


if __name__ == '__main__':
    bot.infinity_polling()
