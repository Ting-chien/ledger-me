from flask import render_template
from app.transactions.models import Transaction

from . import blueprint


@blueprint.route("/", methods=["GET"])
def index():
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).all()
    return render_template("transactions/index.html", transactions=transactions)