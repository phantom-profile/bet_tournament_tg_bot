from pathlib import Path

import telebot
from telebot.types import Message

from bot_app.ui_components import participant_keyboard, init_payment_keyboard, start_keyboard
from bot_app.user import User
from config import locale
from lib.backend_client import BackendClient, Red


MB = 1 * 1024 * 1024


def _save_file(filename: str, content: bytes):
    new_file = Path('uploaded', filename)
    with new_file.open('wb') as file:
        file.write(content)


def _validate_message(message: Message, client: BackendClient) -> str | None:
    if client.in_current_tournament(message.from_user.id):
        return locale.read('already_participate')

    if not Red.exists(f"lock-interface-{message.from_user.id}"):
        return locale.read('no_file_need')

    if not message.document:
        return locale.read('no_file_exists')

    if message.document.file_size > MB:
        return locale.read('file_size_limit')


def init_registration(user: User, bot: telebot.TeleBot):
    if user.is_participant:
        return bot.send_message(
            chat_id=user.id,
            text=locale.read('already_participate'),
            reply_markup=participant_keyboard())

    if not user.client.is_registration_opened():
        return bot.send_message(
            chat_id=user.id,
            text=locale.read('registration_closed'),
            reply_markup=start_keyboard()
        )

    return bot.send_message(
        chat_id=user.id,
        text=locale.read('register_instruction'),
        reply_markup=init_payment_keyboard()
    )


def block_interface(user: User, bot: telebot.TeleBot):
    user.block()
    bot.send_message(chat_id=user.id, text=locale.read('pay_proof_message'))


def get_payment_from_user(message: Message, bot: telebot.TeleBot):
    client = BackendClient()
    error = _validate_message(message, client)
    if error:
        return bot.send_message(message.from_user.id, error)

    file_info = bot.get_file(message.document.file_id)
    content = bot.download_file(file_info.file_path)

    _save_file(message.document.file_name, content)

    bot.send_message(message.from_user.id, locale.read('proof_sent'), reply_markup=participant_keyboard())
    Red.delete(f"lock-interface-{message.from_user.id}")
    client.register(message.from_user.id)
