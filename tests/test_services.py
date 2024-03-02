from bot_app.ui_components import Keyboards
from lib.current_service import CurrentTournamentsService
from lib.registration_controller import (BlockUntilPayService,
                                         GetInstructionsService,
                                         SavePaymentService,)
from lib.spam_protection import SpamProtector
from lib.status_service import CheckStatusService
from tests.factories import ResponceFactory, TournamentFactory, UserFactory, DocumentFactory


def test_spam_protection_service_allow_warn_and_block():
    user_id = 123
    for i in range(SpamProtector.LIMIT - 1):
        assert SpamProtector(user_id).decision() == SpamProtector.ALLOW
    assert SpamProtector(user_id).decision() == SpamProtector.WARN
    assert SpamProtector(user_id).decision() == SpamProtector.FORBID


class TestStatusService:
    def call_service(self, user, ui):
        CheckStatusService(user=user, ui=ui).call()

    def test_for_member(self, success_client, ui_stub):
        user = UserFactory(member=True)
        self.call_service(user, ui_stub)
        ui_stub.send.assert_called_once_with(message='member status', keyboard=Keyboards.MEMBER)

    def test_for_guest(self, success_client, ui_stub):
        user = UserFactory(guest=True)
        self.call_service(user, ui_stub)
        ui_stub.send.assert_called_once_with(message='viewer status', keyboard=Keyboards.START)

    def test_for_closed_tournament(self, ui_stub, empty_tournament_as_json, backend_client):
        user = UserFactory(guest=True)
        response = ResponceFactory.create(body=empty_tournament_as_json)
        backend_client.get_current_tournaments.return_value = response
        self.call_service(user, ui_stub)
        ui_stub.send.assert_called_once_with(message='registration closed error', keyboard=Keyboards.START)


class TestCurrentTournamentService:
    def test_success_response(self, success_client):
        result = CurrentTournamentsService().call()

        assert result is not None
        assert result.name == 't_name'
        assert result.starts_at.year == 2024
        assert result.is_full() is False
        assert result.members_ids == {'1', '2'}
        assert result.is_member(1) is True
        assert result.is_member(3) is False

    def test_if_does_not_exist(self, backend_client, empty_tournament_as_json):
        response = ResponceFactory.create(body=empty_tournament_as_json)
        backend_client.get_current_tournaments.return_value = response
        result = CurrentTournamentsService().call()
        assert result is None


class TestInstructionsService:
    def setup_method(self, _method=None, limit=3, tg_id=1):
        self.tournament = TournamentFactory.create(members_limit=limit)
        self.user = UserFactory.create(tg_id=tg_id)

    def call_service(self):
        return GetInstructionsService(user=self.user, tournament=self.tournament).call()

    def test_no_tournament(self):
        self.tournament = None
        result = self.call_service()
        assert result.message == 'registration closed error'
        assert result.keyboard == Keyboards.START

    def test_member(self):
        result = self.call_service()
        assert result.message == 'member status'
        assert result.keyboard == Keyboards.MEMBER

    def test_full(self):
        self.setup_method(tg_id=10)
        result = self.call_service()
        assert result.message == 'tournament is full error'
        assert result.keyboard == Keyboards.START

    def test_request_membership(self):
        self.setup_method(limit=5, tg_id=10)
        result = self.call_service()
        assert result.message == 'register instruction'
        assert result.keyboard == Keyboards.REQUEST


class TestBlockUntilPayService:
    def setup_method(self, _method):
        self.tournament = TournamentFactory.create(members_limit=5)
        self.user = UserFactory.create(tg_id=10)

    def call_service(self):
        return BlockUntilPayService(user=self.user, tournament=self.tournament).call()

    def test_success_registration(self, success_client):
        result = self.call_service()

        success_client.register.assert_called_once_with(
            user_id=self.user.id,
            user_name=self.user.nick,
            current=self.tournament.id
        )
        assert self.user.is_on_hold is True
        assert result.message == 'payment request message'
        assert result.keyboard is None

    def test_failed_registration(self, failed_client):
        result = self.call_service()

        failed_client.register.assert_called_once_with(
            user_id=self.user.id,
            user_name=self.user.nick,
            current=self.tournament.id
        )
        assert self.user.is_on_hold is False
        assert result.message == 'default error'
        assert result.keyboard is None


class TestSavePaymentService:
    def setup_method(self, _method):
        self.user = UserFactory.create()
        self.user.block()
        self.tournament = TournamentFactory.create()
        self.document = DocumentFactory.create()

    def call_service(self, downloader):
        self.result = SavePaymentService(self.user, self.tournament, self.document, downloader).call()

    def test_no_file_need(self, success_client, downloader_stub):
        self.user.activate()
        self.call_service(downloader_stub)
        success_client.upload_file.assert_not_called()
        assert self.result.message == 'no file need error'
        assert self.user.is_active is True

    def test_no_file_exists(self, success_client, downloader_stub):
        self.document = None
        self.call_service(downloader_stub)
        success_client.upload_file.assert_not_called()
        assert self.result.message == 'no file exists error'
        assert self.user.is_active is False

    def test_file_too_big(self, success_client, downloader_stub):
        self.document = DocumentFactory.create(file_size=1024 * 1024 + 1)
        self.call_service(downloader_stub)
        success_client.upload_file.assert_not_called()
        assert self.result.message == 'file size limit error'
        assert self.user.is_active is False

    def test_success_upload(self, success_client, downloader_stub):
        self.call_service(downloader_stub)
        success_client.upload_file.assert_called_once_with(self.tournament.id, self.user.id, b'content')
        assert self.result.message == 'payment file sent'
        assert self.user.is_active is True
        assert self.result.keyboard == Keyboards.MEMBER

    def test_failed_upload(self, failed_client, downloader_stub):
        self.call_service(downloader_stub)
        failed_client.upload_file.assert_called()
        assert self.result.message == 'default error'
        assert self.user.is_active is False


class TestRegistrationController:
    def test_get_instructions(self):
        pass

    def test_block_until_pay(self):
        pass

    def test_block_until_pay_if_no_tournament(self):
        pass

    def test_pay(self):
        pass
