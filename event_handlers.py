from telebot import TeleBot
from telebot.types import Message

from bot_app.info_providing import initial_info, check_status, rules_info
from bot_app.tournament_registration import init_registration, block_interface, get_payment_from_user

from config import env_variables, locale
from lib.base_client import Red


bot = TeleBot(env_variables.get('TG_BOT_TOKEN'), parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    if Red.exists(f"lock-interface-{message.from_user.id}"):
        bot.send_message(message.from_user.id, locale.read('pay_proof_message'))
        return

    initial_info(message.chat.id, bot)


@bot.message_handler(content_types=['text'])
def message_reply(message: Message):
    print(message.text)
    if Red.exists(f"lock-interface-{message.from_user.id}"):
        bot.send_message(message.chat.id, locale.read('pay_proof_message'))
        return

    if message.text == locale.read('rules'):
        rules_info(message.chat.id, bot)
    elif message.text == locale.read('register'):
        init_registration(message.from_user.id, bot)
    elif message.text == locale.read('status'):
        check_status(message.from_user.id, bot)
    elif message.text == locale.read('request_pay_proof'):
        block_interface(message.from_user.id, bot)


@bot.message_handler(content_types=['document'])
def get_payment_proof(message: Message):
    get_payment_from_user(message, bot)


if __name__ == '__main__':
    bot.infinity_polling()
