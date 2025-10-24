import os

from app import create_app
from app.transactions.models import Transactions
from config import config

ENV = os.getenv('FLASK_ENV', 'development')


try:
    app_config = config[ENV]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, ...]')

app = create_app(app_config)