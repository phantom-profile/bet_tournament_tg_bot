import json

import fakeredis
import pytest
from pytest_mock import MockerFixture

from bot_app.message_sender import MessageSender
from config.setup import BASE_DIR
from lib import base_client
from lib.backend_client import BackendClient
from lib.registration_controller import GetFileService
from tests.factories import ResponceFactory


@pytest.fixture(autouse=True)
def patch_redis_global(monkeypatch):
    # Patch the 'Red' global variable with the fake Redis client
    monkeypatch.setattr(base_client.Red, 'conn', fakeredis.FakeRedis())


@pytest.fixture
def ui_stub(mocker):
    return mocker.MagicMock(spec=MessageSender)


@pytest.fixture
def downloader_stub(mocker):
    mock_service = mocker.MagicMock(spec=GetFileService)
    mocker.patch.object(GetFileService, "__new__", return_value=mock_service)
    mock_service.call.return_value = b'content'
    return mock_service


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
    response = ResponceFactory.create(body={}, status=201)
    backend_client.register.return_value = response
    backend_client.upload_file.return_value = response
    return backend_client


@pytest.fixture
def failed_client(backend_client):
    response = ResponceFactory.create(failed=True)
    backend_client.get_current_tournaments.return_value = response
    backend_client.register.return_value = response
    backend_client.upload_file.return_value = response
    return backend_client
