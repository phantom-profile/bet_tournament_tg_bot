import json

import fakeredis
import pytest
from pytest_mock import MockerFixture

from bot_app.message_sender import MessageSender
from lib.backend_client import BackendClient
from lib import base_client

from config.setup import BASE_DIR
from tests.factories import ResponceFactory, UserFactory


@pytest.fixture(autouse=True)
def patch_redis_global(monkeypatch):
    # Patch the 'Red' global variable with the fake Redis client
    monkeypatch.setattr(base_client.Red, 'conn', fakeredis.FakeRedis())


@pytest.fixture
def ui_stub(mocker):
    return mocker.MagicMock(spec=MessageSender)


@pytest.fixture
def backend_client(mocker: MockerFixture):
    mock_client = mocker.MagicMock(spec=BackendClient)
    # Patch the creation of new BackendClient instances to return the mock_client
    mocker.patch.object(BackendClient, "__new__", return_value=mock_client)
    return mock_client


@pytest.fixture
def tournament_as_json():
    with (BASE_DIR / 'tests' / 'responses' / 'current_tournaments.json').open() as f:
        return json.load(f)


@pytest.fixture
def empty_tournament_as_json():
    with (BASE_DIR / 'tests' / 'responses' / 'empty_current_tournaments.json').open() as f:
        return json.load(f)


@pytest.fixture
def success_client(backend_client, tournament_as_json, empty_tournament_as_json):
    response = ResponceFactory.create(body=tournament_as_json)
    backend_client.get_current_tournaments.return_value = response
    return backend_client
