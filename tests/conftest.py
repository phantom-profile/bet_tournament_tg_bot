import json

import fakeredis
import pytest
from pytest_mock import MockerFixture
from telebot import TeleBot

from bot_app.message_sender import MessageSender
from config.setup import BASE_DIR
from lib import base_client
from lib.backend_client import BackendClient
from tests.factories import FileFactory, ResponceFactory


@pytest.fixture(autouse=True)
def prepare_infra(monkeypatch):
    # Patch the 'Red' global variable with the fake Redis client
    monkeypatch.setenv('API_ACCESS_TOKEN', 'TEST_TOKEN')
    monkeypatch.setattr(base_client.Red, 'conn', fakeredis.FakeRedis())


@pytest.fixture
def ui_stub(mocker):
    mock_service = mocker.MagicMock(spec=MessageSender)
    mocker.patch.object(MessageSender, "__new__", return_value=mock_service)
    return mock_service


@pytest.fixture
def backend_client(mocker: MockerFixture):
    mock_client = mocker.MagicMock(spec=BackendClient)
    # Patch the creation of new BackendClient instances to return the mock_client
    mocker.patch.object(BackendClient, "__new__", return_value=mock_client)
    return mock_client


@pytest.fixture
def bot_stub(mocker: MockerFixture):
    mock_client = mocker.MagicMock(spec=TeleBot)
    mocker.patch.object(TeleBot, "__new__", return_value=mock_client)
    mock_client.get_file.return_value = FileFactory.create()
    mock_client.download_file.return_value = b'content'
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
