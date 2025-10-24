from flask import Blueprint

blueprint = Blueprint(
    'transactions',
    __name__,
    url_prefix='/transactions'
)
