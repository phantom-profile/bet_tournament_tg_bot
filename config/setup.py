import gettext
import logging
from os import getenv

from json import load
from pathlib import Path
from typing import Callable

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.logging import ignore_logger

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    CONF_FILE = BASE_DIR / 'config' / 'config.json'
    ENV_FILE = BASE_DIR / 'config' / '.env'
    LOCALE_DIR = BASE_DIR / 'locales'

    def __init__(self):
        self._config = self._load_data()
        self.log_options = self._log_options()

    def _load_data(self) -> dict[str, str]:
        with self.CONF_FILE.open() as json_data:
            config = load(json_data)
        common = config['common']
        if config['is_production']:
            extra = config['prod']
        else:
            extra = config['dev']
        return common | extra | {'is_production': config['is_production']}

    def _log_options(self):
        options = {
            'level': logging.INFO,
            'format': self.log_format,
            'filemode': self.log_filemode
        }
        if self.logger == 'file':
            options['filename'] = BASE_DIR / 'log' / self.log_file
        return options

    def __getattr__(self, item: str) -> str:
        return self._config[item]

    def __str__(self) -> str:
        return str(self._config)


app_conf = Config()
load_dotenv(app_conf.ENV_FILE)


def set_locale() -> Callable[[str], str]:
    locale = gettext.translation('app', localedir=Config.LOCALE_DIR, languages=[app_conf.locale])
    locale.install()
    return locale.gettext


def set_logger():
    ignored_logger = logging.getLogger("TeleBot")
    ignored_logger.disabled = True
    logging.basicConfig(**app_conf.log_options)
    logging.info(f'Logger set with options {app_conf.log_options}')


set_logger()
logging.info('locale file initialize')
lc = set_locale()
if getenv('SENTRY_TOKEN') and app_conf.is_production:
    logging.info('sentry initialize')

    ignore_logger("TeleBot")
    sentry_sdk.init(
        dsn=getenv('SENTRY_TOKEN'),
        # percentage of sent to Sentry errors
        traces_sample_rate=app_conf.traces_sample_rate,
    )
else:
    logging.warning('NO SENTRY CONFIG PRESENTS!!!')
