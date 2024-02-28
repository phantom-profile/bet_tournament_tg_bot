from bot_app.message_sender import MessageSender
from bot_app.ui_components import Keyboards
from bot_app.user import User
from lib.current_service import CurrentTournamentsService


class CheckStatusService:
    def __init__(self, user: User, ui: MessageSender):
        self.user = user
        self.ui = ui

    def call(self):
        tournament = CurrentTournamentsService().call()
        if not tournament:
            return self.ui.send(message='registration closed error', keyboard=Keyboards.START)

        if tournament.is_member(self.user.id):
            return self.ui.send(message='member status', keyboard=Keyboards.MEMBER)

        self.ui.send(message='viewer status', keyboard=Keyboards.START)
