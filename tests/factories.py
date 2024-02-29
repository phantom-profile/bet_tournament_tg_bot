import factory
import faker

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

    @factory.lazy_attribute
    def members_count(self):
        return len(self.members_ids)
