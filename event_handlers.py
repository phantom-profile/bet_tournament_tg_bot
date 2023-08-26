from telebot import TeleBot
from telebot.types import Message

from bot_app.info_providing import initial_info, check_status, rules_info
from bot_app.tournament_registration import init_registration, block_interface, get_payment_from_user

from config import env_variables, locale
from lib.base_client import Red


bot = TeleBot(env_variables.get('TG_BOT_TOKEN'), parse_mode=None)


class User:
    def __init__(self, user_id: int):
        self.id = user_id

    @property
    def is_temp_blocked(self) -> bool:
        return Red.exists(f"lock-interface-{self.id}")


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    user = User(message.from_user.id)
    if user.is_temp_blocked:
        return bot.send_message(user.id, locale.read('pay_proof_message'))

    initial_info(message.chat.id, bot)


@bot.message_handler(content_types=['text'])
def message_reply(message: Message):
    print(message.text)
    user = User(message.from_user.id)
    if user.is_temp_blocked:
        return bot.send_message(user.id, locale.read('pay_proof_message'))

    if message.text == locale.read('rules'):
        rules_info(user.id, bot)
    elif message.text == locale.read('register'):
        init_registration(user.id, bot)
    elif message.text == locale.read('status'):
        check_status(user.id, bot)
    elif message.text == locale.read('request_pay_proof'):
        block_interface(user.id, bot)


@bot.message_handler(content_types=['document'])
def get_payment_proof(message: Message):
    get_payment_from_user(message, bot)


if __name__ == '__main__':
    bot.infinity_polling()
