import factory

from lib.base_client import Response


class ResponceFactory(factory.Factory):
    class Meta:
        model = Response
        exclude = ('failed',)

    status = 200
    request_url = 'https://backend.com/path/to/endpoint'
    body = factory.LazyAttribute(lambda: {"data": {}})

    failed = factory.Trait(
        status=500,
        body={"error": "error on server happened"}
    )

    @factory.lazy_attribute
    def is_successful(self):
        return self.status == 200
