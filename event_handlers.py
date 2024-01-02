from telebot import TeleBot
from telebot.types import Message

from bot_app.message_sender import MessageSender
from bot_app.ui_components import start_keyboard
from bot_app.user import User
from config.setup import env_variables, lc
from lib.app_logging import log_tg_message, logger_factory
from lib.registration_controller import RegistrationController
from lib.status_service import CheckStatusService

bot = TeleBot(env_variables.get('TG_BOT_TOKEN'), parse_mode=None)
logger = logger_factory()


@bot.message_handler(commands=['start'])
@logger
def send_welcome(message: Message):
    user = User(message.from_user)
    ui = MessageSender(bot, message.chat.id)
    if user.is_on_hold:
        return ui.send(message='payment request message')

    ui.send(message='start bot', keyboard=start_keyboard())


@bot.message_handler(content_types=['text'])
@logger
def message_reply(message: Message):
    log_tg_message(message)
    user = User(message.from_user)
    ui = MessageSender(bot, message.chat.id)
    if user.is_on_hold:
        return ui.send(message='payment request message')

    if message.text == lc('rules button'):
        ui.send(message='membership rules')
    elif message.text == lc('status button'):
        CheckStatusService(user, message, bot).call()
    elif message.text == lc('registration button'):
        RegistrationController(user, message, bot).get_instructions()
    elif message.text == lc('request membership button'):
        RegistrationController(user, message, bot).block_unlit_pay()


@bot.message_handler(content_types=['document'])
@logger
def get_payment_proof(message: Message):
    log_tg_message(message)
    user = User(message.from_user)
    RegistrationController(user, message, bot).pay()


if __name__ == '__main__':
    bot.infinity_polling()
