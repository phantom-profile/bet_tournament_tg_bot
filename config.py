from pathlib import Path
from dotenv import dotenv_values

import sentry_sdk
from sentry_sdk.integrations.logging import ignore_logger

from lib.locale_service import LocaleService

env_variables = dotenv_values(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
LOCALE = 'ru'
locale = LocaleService(BASE_DIR / 'locale.json', LOCALE)


if env_variables.get('SENTRY_TOKEN'):
    print('sentry initialize')
    ignore_logger("TeleBot")
    sentry_sdk.init(
        dsn=env_variables.get('SENTRY_TOKEN'),
        # percentage of sent to Sentry errors
        traces_sample_rate=1.0,
    )
else:
    print('WARN: NO SENTRY CONFIG PRESENTS!!!')
