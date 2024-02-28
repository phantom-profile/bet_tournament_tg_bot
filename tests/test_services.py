from bot_app.ui_components import Keyboards
from lib.current_service import CurrentTournamentsService
from lib.spam_protection import SpamProtector
from lib.status_service import CheckStatusService
from tests.factories import ResponceFactory, UserFactory


def test_status_for_member(success_client, ui_stub):
    user = UserFactory(member=True)
    CheckStatusService(user=user, ui=ui_stub).call()
    ui_stub.send.assert_called_once_with(message='member status', keyboard=Keyboards.MEMBER)


def test_status_for_guest(success_client, ui_stub):
    user = UserFactory(guest=True)
    CheckStatusService(user=user, ui=ui_stub).call()
    ui_stub.send.assert_called_once_with(message='viewer status', keyboard=Keyboards.START)


def test_status_for_closed_tournament(backend_client, empty_tournament_as_json, ui_stub):
    user = UserFactory(guest=True)
    response = ResponceFactory.create(body=empty_tournament_as_json)
    backend_client.get_current_tournaments.return_value = response
    CheckStatusService(user=user, ui=ui_stub).call()
    ui_stub.send.assert_called_once_with(message='registration closed error', keyboard=Keyboards.START)


def test_get_current_tournament(success_client, tournament_as_json):
    result = CurrentTournamentsService().call()

    assert result is not None
    assert result.name == 't_name'
    assert result.starts_at.year == 2024
    assert result.is_full() is False
    assert result.members_ids == {'1', '2'}
    assert result.is_member(1) is True
    assert result.is_member(3) is False


def test_get_current_tournament_if_does_not_exist(backend_client, empty_tournament_as_json):
    response = ResponceFactory.create(body=empty_tournament_as_json)
    backend_client.get_current_tournaments.return_value = response
    result = CurrentTournamentsService().call()
    assert result is None


def test_spam_protection_service_allow_warn_and_block():
    user_id = 123
    for i in range(SpamProtector.LIMIT - 1):
        assert SpamProtector(user_id).decision() == SpamProtector.ALLOW
    assert SpamProtector(user_id).decision() == SpamProtector.WARN
    assert SpamProtector(user_id).decision() == SpamProtector.FORBID
