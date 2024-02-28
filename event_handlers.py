from telebot import TeleBot
from telebot.types import Message

from bot_app.message_sender import MessageSender
from bot_app.ui_components import Keyboards
from bot_app.user import User
from config.setup import env_variables, lc
from lib.app_logging import log_tg_message, logger_factory
from lib.registration_controller import RegistrationController
from lib.spam_protection import control_rate_limit
from lib.status_service import CheckStatusService

bot = TeleBot(env_variables.get('TG_BOT_TOKEN'), parse_mode=None)
logger = logger_factory()
protector = control_rate_limit(bot)


@bot.message_handler(commands=['start'])
@protector
@logger
def send_welcome(message: Message):
    user = User(tg_id=message.from_user.id, nick=message.from_user.username)
    ui = MessageSender(bot, message.chat.id)
    if user.is_on_hold:
        return ui.send(message='payment request message')

    ui.send(message='start bot', keyboard=Keyboards.START)


@bot.message_handler(content_types=['text'])
@protector
@logger
def message_reply(message: Message):
    log_tg_message(message)
    user = User(tg_id=message.from_user.id, nick=message.from_user.username)
    ui = MessageSender(bot, message.chat.id)
    if user.is_on_hold:
        return ui.send(message='payment request message')

    if message.text == lc('rules button'):
        ui.send(message='membership rules')
    elif message.text == lc('status button'):
        CheckStatusService(user, ui).call()
    elif message.text == lc('registration button'):
        RegistrationController(user, message, bot).get_instructions()
    elif message.text == lc('request membership button'):
        RegistrationController(user, message, bot).block_until_pay()


@bot.message_handler(content_types=['document'])
@protector
@logger
def get_payment_proof(message: Message):
    log_tg_message(message)
    user = User(tg_id=message.from_user.id, nick=message.from_user.username)
    RegistrationController(user, message, bot).pay()


if __name__ == '__main__':
    bot.infinity_polling()
