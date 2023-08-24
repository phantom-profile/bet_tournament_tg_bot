import telebot
from telebot.types import Message

from config import env_variables
from lib.locale_service import LocaleService


bot = telebot.TeleBot(env_variables.get('TG_BOT_TOKEN'), parse_mode=None)
localizator = LocaleService()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    print(message.chat.id)
    bot.reply_to(message, localizator.read('start'))


if __name__ == '__main__':
    bot.infinity_polling()
