from json import load

from config import BASE_DIR, LOCALE


class LocaleService:
    def __init__(self):
        self.messages = load(open(BASE_DIR / 'locale.json'))[LOCALE]

    def read(self, key):
        return self.messages[key]
