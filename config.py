from pathlib import Path
from dotenv import dotenv_values

env_variables = dotenv_values(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
