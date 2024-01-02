from telebot import TeleBot

from config.setup import lc


class MessageSender:
    def __init__(self, bot: TeleBot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    def send(self, message, keyboard=None):
        self.bot.send_message(text=lc(message), chat_id=self.chat_id, reply_markup=keyboard)
