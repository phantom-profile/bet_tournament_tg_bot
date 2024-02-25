from lib.current_service import CurrentTournamentsService
from tests.factories import ResponceFactory
from tests.helpers import tournament_payload


def test_status_receiving():
    pass


def test_get_current_tournament(backend_client):
    members = [
        {'status': 'registered', 'tg_id': '123-123'},
        {'status': 'approved', 'tg_id': '223-223'},
        {'status': 'declined', 'tg_id': '323-323'}
    ]
    payload = tournament_payload(members=members, name='t_name')
    response = ResponceFactory.create(body=payload)
    backend_client.get_current_tournaments.return_value = response

    result = CurrentTournamentsService().call()

    assert result is not None
    assert result.name == 't_name'
    assert result.is_full() is False
    assert result.members_ids == {'123-123', '223-223'}
    assert result.is_member('123-123') is True
    assert result.is_member('323-323') is False


def test_get_current_tournament_if_does_not_exist(backend_client):
    payload = tournament_payload(no_data=True)
    response = ResponceFactory.create(body=payload)
    backend_client.get_current_tournaments.return_value = response
    result = CurrentTournamentsService().call()
    assert result is None
