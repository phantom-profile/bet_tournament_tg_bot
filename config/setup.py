import logging
from pathlib import Path
from json import load
from dotenv import dotenv_values

import sentry_sdk
from sentry_sdk.integrations.logging import ignore_logger

from lib.locale_service import LocaleService


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    CONF_FILE = BASE_DIR / 'config' / 'config.json'
    ENV_FILE = BASE_DIR / 'config' / '.env'
    LOCALE_FILE = BASE_DIR / 'config' / 'locale.json'

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
locale = LocaleService(app_conf.LOCALE_FILE, app_conf.locale)
env_variables = dotenv_values(app_conf.ENV_FILE)


def set_logger():
    ignored_logger = logging.getLogger("TeleBot")
    ignored_logger.disabled = True
    logging.basicConfig(**app_conf.log_options)
    logging.info(f'Logger set with options {app_conf.log_options}')


set_logger()
if env_variables.get('SENTRY_TOKEN'):
    logging.info('sentry initialize')

    ignore_logger("TeleBot")
    sentry_sdk.init(
        dsn=env_variables.get('SENTRY_TOKEN'),
        # percentage of sent to Sentry errors
        traces_sample_rate=app_conf.traces_sample_rate,
    )
else:
    logging.warning('NO SENTRY CONFIG PRESENTS!!!')
