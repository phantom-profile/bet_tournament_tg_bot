import telebot
from telebot.types import Message
from dotenv import dotenv_values

env_variables = dotenv_values(".env")

bot = telebot.TeleBot(env_variables.get('TG_BOT_TOKEN'), parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    print(message.chat.id)
    bot.reply_to(message, "salam alleykum, ebana!")


if __name__ == '__main__':
    bot.infinity_polling()
