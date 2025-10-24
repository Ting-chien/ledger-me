from flask import render_template, request, redirect, url_for

from . import blueprint
from .models import Transaction
from app import db


@blueprint.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle form submission for creating a new transaction
        item = request.form.get("item")
        transaction_type = request.form.get("type")
        expense = request.form.get("expense")
        transaction_at = request.form.get("date")
        # Create and save the new transaction
        new_transaction = Transaction(
            item=item,
            type=transaction_type,
            expense=expense,
            transaction_at=transaction_at
        )
        db.session.add(new_transaction)
        db.session.commit()
        return redirect(url_for("transactions.index"))
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).all()
    return render_template("transactions/index.html", transactions=transactions)