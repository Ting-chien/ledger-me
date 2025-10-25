from flask import Blueprint

blueprint = Blueprint(
    'reports',
    __name__,
    url_prefix='/reports'
)
