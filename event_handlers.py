from telebot import TeleBot
from telebot.types import Message

from bot_app.info_providing import initial_info, check_status, rules_info
from bot_app.tournament_registration import init_registration, block_interface, get_payment_from_user
from bot_app.user import User

from config import env_variables, locale


bot = TeleBot(env_variables.get('TG_BOT_TOKEN'), parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    user = User(message.from_user.id)
    if user.is_temp_blocked:
        return bot.send_message(user.id, locale.read('pay_proof_message'))

    initial_info(user.id, bot)


@bot.message_handler(content_types=['text'])
def message_reply(message: Message):
    print(message.text)
    user = User(message.from_user.id)
    if user.is_temp_blocked:
        return bot.send_message(user.id, locale.read('pay_proof_message'))

    if message.text == locale.read('rules'):
        rules_info(user.id, bot)
    elif message.text == locale.read('register'):
        init_registration(user, bot)
    elif message.text == locale.read('status'):
        check_status(user, bot)
    elif message.text == locale.read('request_pay_proof'):
        block_interface(user, bot)


@bot.message_handler(content_types=['document'])
def get_payment_proof(message: Message):
    get_payment_from_user(message, bot)


if __name__ == '__main__':
    bot.infinity_polling()
