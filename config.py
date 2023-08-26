from pathlib import Path
from dotenv import dotenv_values

from lib.locale_service import LocaleService

env_variables = dotenv_values(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
LOCALE = 'ru'
locale = LocaleService(BASE_DIR / 'locale.json', LOCALE)
