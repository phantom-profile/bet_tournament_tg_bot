import factory
import faker

from lib.base_client import Response
from bot_app.user import User

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
        return self.status == 200


class UserFactory(factory.Factory):
    tg_id = factory.LazyAttribute(lambda _: generator.random_int())
    nick = factory.LazyAttribute(lambda _: generator.name())

    class Meta:
        model = User

    class Params:
        member = factory.Trait(tg_id=1)
        guest = factory.Trait(tg_id=3)
