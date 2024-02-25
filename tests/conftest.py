import fakeredis
import pytest
from pytest_mock import MockerFixture

from bot_app.message_sender import MessageSender
from lib.backend_client import BackendClient
from tests.helpers import TgTestBot


@pytest.fixture(autouse=True)
def patch_redis_global(monkeypatch):
    # Patch the 'Red' global variable with the fake Redis client
    monkeypatch.setattr('lib.base_client.Red', fakeredis.FakeRedis())


@pytest.fixture
def bot_stub():
    return TgTestBot()


@pytest.fixture
def ui(bot_stub):
    return MessageSender(bot_stub, chat_id='12345')


@pytest.fixture
def backend_client(mocker: MockerFixture):
    mock_client = mocker.MagicMock(spec=BackendClient)
    # Patch the creation of new BackendClient instances to return the mock_client
    mocker.patch.object(BackendClient, "__new__", return_value=mock_client)
    return mock_client
