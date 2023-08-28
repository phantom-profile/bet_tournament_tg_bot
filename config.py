import logging
from pathlib import Path
from dotenv import dotenv_values

import sentry_sdk
from sentry_sdk.integrations.logging import ignore_logger

from lib.locale_service import LocaleService

env_variables = dotenv_values(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
LOCALE = 'ru'
LOGGER = 'file'
locale = LocaleService(BASE_DIR / 'locale.json', LOCALE)


def set_logger():
    options = {
        'level': logging.INFO,
        'format': '%(asctime)s %(levelname)s %(message)s',
        'filemode': 'w'
    }

    ignored_logger = logging.getLogger("TeleBot")
    ignored_logger.disabled = True

    if LOGGER == 'file':
        options['filename'] = BASE_DIR / 'log' / 'bot_log.log'
    logging.basicConfig(**options)
    logging.info(f'Logger set with options {options}')


set_logger()
if env_variables.get('SENTRY_TOKEN'):
    logging.info('sentry initialize')

    ignore_logger("TeleBot")
    sentry_sdk.init(
        dsn=env_variables.get('SENTRY_TOKEN'),
        # percentage of sent to Sentry errors
        traces_sample_rate=1.0,
    )
else:
    logging.warning('NO SENTRY CONFIG PRESENTS!!!')
