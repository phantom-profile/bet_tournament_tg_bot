from json import load


class LocaleService:
    def __init__(self, locale_path, locale: str):
        self.messages = load(locale_path.open())[locale]

    def read(self, key: str) -> str:
        return self.messages[key]
