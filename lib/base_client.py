import logging
import redis

from dataclasses import dataclass
from json import dumps, loads
from typing import Any, Optional

from requests import Response as HttpResponse
from requests import exceptions

from lib.app_logging import log_text

# Redis documentation - https://redis.io/docs/clients/python/


class Red:
    conn = redis.Redis(host='localhost', port=6379, decode_responses=True)


class CacheService:
    def __init__(self):
        self.__key = None

    @property
    def key(self):
        if not self.__key:
            raise NotImplementedError('add key through .set_key("my-key")')
        return self.__key

    def set_key(self, key: str):
        self.__key = key

    def is_exist(self):
        return Red.conn.exists(self.key) > 0

    def get_cached(self):
        if not self.is_exist():
            return None
        return loads(Red.conn.get(self.key))

    def save(self, jsonable: dict, time: int = None):
        if time:
            Red.conn.setex(self.key, time, dumps(jsonable))
            return
        Red.conn.set(self.key, dumps(jsonable))


@dataclass
class Response:
    status: int
    request_url: str
    is_successful: bool
    body: dict[str, Any]


class BaseClient:
    URL = ''
    TOKEN = ''

    def __init__(self):
        if not self.TOKEN:
            raise AttributeError('API token is empty! Add it to .env config')

        self._response: Optional[HttpResponse] = None
        self.cacher = CacheService()

    # FOR INTERNAL USAGE ONLY
    @property
    def _service_response(self) -> Response:
        response = Response(
            status=self._response.status_code,
            request_url=self._response.url,
            is_successful=self._is_successful,
            body=self._parsed_response
        )
        params = {'level': logging.INFO, 'sentry': False} if response.is_successful else {}
        log_text(str(response), **params)
        return response

    def _build_url(self, path: str, request_format: str = None):
        if not request_format:
            return f'{self.URL}/{path}'
        return f'{self.URL}/{path}.{request_format}'

    @property
    def _is_successful(self):
        return 200 <= self._response.status_code < 300

    @property
    def _parsed_response(self):
        try:
            return self._response.json()
        except exceptions.JSONDecodeError:
            return {
                "error": {
                    "message": "impossible to decode to JSON",
                    "original_text": self._response.text}
            }
