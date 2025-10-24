import os

from app import create_app, db
from app.transactions.models import Transaction, TransactionCategory
from config import config

ENV = os.getenv('FLASK_ENV', 'development')


try:
    app_config = config[ENV]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, ...]')

app = create_app(app_config)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Transaction=Transaction, TransactionCategory=TransactionCategory)