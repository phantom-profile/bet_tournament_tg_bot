import telebot
from telebot import types
from telebot.types import Message

from config import env_variables
from lib.locale_service import LocaleService
from lib.backend_client import BackendClient


bot = telebot.TeleBot(env_variables.get('TG_BOT_TOKEN'), parse_mode=None)
localizator = LocaleService()


def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rules = types.KeyboardButton(text=localizator.read('rules'))
    register = types.KeyboardButton(text=localizator.read('register'))
    status = types.KeyboardButton(text=localizator.read('status'))
    keyboard.add(rules, register, status)
    return keyboard


def participant_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    make_bet = types.KeyboardButton(text=localizator.read('make_bet'))
    rules = types.KeyboardButton(text=localizator.read('rules'))
    status = types.KeyboardButton(text=localizator.read('status'))
    keyboard.add(make_bet, rules, status)
    return keyboard


def check_status(message: Message):
    print(message.chat.id)
    print(message.from_user.id)
    client = BackendClient()
    if client.in_current_tournament(message.from_user.id):
        return bot.send_message(
            message.chat.id,
            localizator.read('participant'),
            reply_markup=participant_keyboard()
        )

    bot.send_message(message.chat.id, localizator.read('viewer'), reply_markup=start_keyboard())


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    print(message.chat.id)
    bot.send_message(message.chat.id, localizator.read('start'), reply_markup=start_keyboard())


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == localizator.read('rules'):
        bot.send_message(message.chat.id, localizator.read('rules_faq'))
    elif message.text == localizator.read('register'):
        bot.send_message(message.chat.id, localizator.read('register_instruction'))
    elif message.text == localizator.read('status'):
        check_status(message)


if __name__ == '__main__':
    bot.infinity_polling()
