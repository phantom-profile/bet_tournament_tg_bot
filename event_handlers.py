from telebot import TeleBot
from telebot.types import Message

from bot_app.info_providing import initial_info, rules_info
from bot_app.user import User

from config.setup import env_variables, locale
from lib.app_logging import logger_factory, log_tg_message
from lib.registration_service import RegisterOnTournamentService
from lib.status_service import CheckStatusService

bot = TeleBot(env_variables.get('TG_BOT_TOKEN'), parse_mode=None)
logger = logger_factory()


@bot.message_handler(commands=['start'])
@logger
def send_welcome(message: Message):
    user = User(message.from_user)
    if user.is_on_hold:
        return bot.send_message(user.id, locale.read('pay_proof_message'))

    initial_info(user.id, bot)


@bot.message_handler(content_types=['text'])
@logger
def message_reply(message: Message):
    log_tg_message(message)
    user = User(message.from_user)
    if user.is_on_hold:
        return bot.send_message(user.id, locale.read('pay_proof_message'))

    if message.text == locale.read('rules'):
        rules_info(user.id, bot)
    elif message.text == locale.read('status'):
        CheckStatusService(user, message, bot).call()
    elif message.text == locale.read('register'):
        RegisterOnTournamentService(user, message, bot).get_instructions()
    elif message.text == locale.read('request_membership'):
        RegisterOnTournamentService(user, message, bot).hold_unlit_payment()


@bot.message_handler(content_types=['document'])
@logger
def get_payment_proof(message: Message):
    log_tg_message(message)
    user = User(message.from_user)
    RegisterOnTournamentService(user, message, bot).pay()


if __name__ == '__main__':
    bot.infinity_polling()
