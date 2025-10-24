from flask import render_template, request, redirect, url_for

from . import blueprint
from .models import Transaction, TransactionCategory
from app import db


@blueprint.route("/", methods=["GET", "POST"])
def index():
    categories = TransactionCategory.query.order_by(TransactionCategory.name.asc()).all()
    if request.method == "POST":
        item = request.form.get("item")
        category_id = request.form.get("category")
        expense = request.form.get("expense")
        transaction_at = request.form.get("date")
        new_transaction = Transaction(
            item=item,
            category_id=category_id if category_id else None,
            expense=expense,
            transaction_at=transaction_at
        )
        db.session.add(new_transaction)
        db.session.commit()
        return redirect(url_for("transactions.index"))
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).all()
    return render_template("transactions/index.html", transactions=transactions, categories=categories)