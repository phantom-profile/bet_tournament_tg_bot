import factory
import faker
from telebot.types import Chat, Document, File, Message

from bot_app.user import User
from lib.base_client import Response
from lib.current_service import Tournament

generator = faker.Faker(use_weighting=False)


class ResponceFactory(factory.Factory):
    class Meta:
        model = Response
        exclude = ()

    status = 200
    request_url = 'https://backend.com/path/to/endpoint'
    body = factory.LazyAttribute(lambda _: {"data": {}})

    class Params:
        failed = factory.Trait(
            status=500,
            body={"error": "error on server happened"}
        )

    @classmethod
    def create(cls, **kwargs) -> Response:
        return super().create(**kwargs)

    @factory.lazy_attribute
    def is_successful(self):
        return 200 <= self.status <= 299


class UserFactory(factory.Factory):
    tg_id = factory.LazyAttribute(lambda _: generator.random_int())
    nick = factory.LazyAttribute(lambda _: generator.name())

    class Meta:
        model = User

    class Params:
        member = factory.Trait(tg_id=1)
        guest = factory.Trait(tg_id=3)

    @classmethod
    def create(cls, **kwargs) -> User:
        return super().create(**kwargs)


class TournamentFactory(factory.Factory):
    class Meta:
        model = Tournament

    id = factory.LazyAttribute(lambda _: generator.random_int())
    name = factory.LazyAttribute(lambda _: generator.name())
    members_limit = factory.LazyAttribute(lambda _: generator.random_int())
    member_cost = factory.LazyAttribute(lambda _: generator.random_int())
    duration = factory.LazyAttribute(lambda _: generator.random_int())
    created_at = factory.LazyAttribute(lambda _: generator.past_datetime())
    starts_at = factory.LazyAttribute(lambda _: generator.future_datetime())
    members_ids = factory.LazyAttribute(lambda _: {'1', '2', '3'})

    @classmethod
    def create(cls, **kwargs) -> Tournament:
        return super().create(**kwargs)

    @factory.lazy_attribute
    def members_count(self):
        return len(self.members_ids)


class DocumentFactory(factory.Factory):
    class Meta:
        model = Document

    file_id = factory.LazyAttribute(lambda _: '1234-1234')
    file_unique_id = factory.LazyAttribute(lambda _: '1234-1234')
    file_name = factory.LazyAttribute(lambda _: 'file.pdf')
    file_size = factory.LazyAttribute(lambda _: 1024)

    @classmethod
    def create(cls, **kwargs) -> Document:
        return super().create(**kwargs)


class MessageFactory(factory.Factory):
    class Meta:
        model = Message

    message_id = factory.LazyAttribute(lambda _: '1234-1234')
    chat = factory.LazyAttribute(lambda _: Chat(id='1234', type='chat'))
    from_user = factory.LazyAttribute(lambda _: UserFactory.create())
    content_type = factory.LazyAttribute(lambda _: 'text')
    json_string = factory.LazyAttribute(lambda _: '{}')
    date = factory.LazyAttribute(lambda _: factory.Faker('datetime'))
    options = factory.LazyAttribute(lambda _: [])

    @classmethod
    def create(cls, **kwargs) -> Message:
        return super().create(**kwargs)


class FileFactory(factory.Factory):
    class Meta:
        model = File

    file_id = factory.LazyAttribute(lambda _: '1234-1234')
    file_path = factory.LazyAttribute(lambda _: '1234-1234')
    file_unique_id = factory.LazyAttribute(lambda _: '1234-1234')
    file_size = factory.LazyAttribute(lambda _: 1024)

    @classmethod
    def create(cls, **kwargs) -> File:
        return super().create(**kwargs)
