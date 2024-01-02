from dataclasses import dataclass

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup

from bot_app.message_sender import MessageSender
from bot_app.ui_components import (participant_keyboard,
                                   request_membership_keyboard, start_keyboard)
from bot_app.user import User
from lib.backend_client import BackendClient
from lib.current_service import CurrentTournamentsService, Tournament

MB = 1 * 1024 * 1024


@dataclass
class ServiceResult:
    message: str
    keyboard: ReplyKeyboardMarkup | None = None


class RegistrationController:
    def __init__(self, user: User, message: Message, bot: TeleBot):
        self.client = BackendClient()
        self.user = user
        self.message = message
        self.bot = bot
        self.ui = MessageSender(bot, chat_id=message.chat.id)

    def get_instructions(self):
        result = GetInstructionsService(self.user, self.tournament).call()
        self.ui.send(message=result.message, keyboard=result.keyboard)

    def block_unlit_pay(self):
        if self.tournament:
            result = BlockUntilPayService(self.user, self.tournament).call()
        else:
            result = GetInstructionsService(self.user, self.tournament).call()
        return self.ui.send(message=result.message, keyboard=result.keyboard)

    def pay(self):
        result = SavePaymentService(
            user=self.user,
            tournament=self.tournament,
            file=self.message.document,
            bot=self.bot
        ).call()
        self.ui.send(message=result.message, keyboard=result.keyboard)

    @property
    def tournament(self):
        if not hasattr(self, '_tournament'):
            self._tournament = CurrentTournamentsService().call()
        return self._tournament


class GetInstructionsService:
    def __init__(self, user: User, tournament: Tournament):
        self.user = user
        self.tournament = tournament

    def call(self):
        if not self.tournament:
            text, keyboard = 'registration closed error', start_keyboard()
        elif self.tournament.is_member(self.user.id):
            text, keyboard = 'member status', participant_keyboard()
        elif self.tournament.is_full():
            text, keyboard = 'tournament is full error', start_keyboard()
        else:
            text, keyboard = 'register instruction', request_membership_keyboard()
        return ServiceResult(text, keyboard=keyboard)


class BlockUntilPayService:
    def __init__(self, user: User, tournament: Tournament):
        self.client = BackendClient()
        self.user = user
        self.tournament = tournament

    def call(self):
        self.user.block()
        response = self.client.register(
            user_id=self.user.id,
            user_name=self.user.nick,
            current=self.tournament.id
        )
        if not response.is_successful:
            self.user.activate()
            return ServiceResult('default error')
        return ServiceResult('payment request message')


class SavePaymentService:
    def __init__(self, user: User, tournament: Tournament, file, bot: TeleBot):
        self.client = BackendClient()
        self.user = user
        self.tournament = tournament
        self.file = file
        self.bot = bot

    def call(self):
        register_error = self._register_error()
        if register_error:
            return ServiceResult(register_error)

        response = self.client.upload_file(self.tournament.id, self.user.id, self._file_content())
        if response.is_successful:
            self.user.activate()
            return ServiceResult('payment file sent', keyboard=participant_keyboard())
        else:
            return ServiceResult('default error')

    def _register_error(self):
        if self.user.is_active:
            return 'no file need error'

        if not self.file:
            return 'no file exists error'

        if self.file.file_size > MB:
            return 'file size limit error'

    def _file_content(self):
        file_info = self.bot.get_file(self.file.file_id)
        return self.bot.download_file(file_info.file_path)
