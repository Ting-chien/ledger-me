from flask import jsonify
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
        remark = request.form.get("remark")
        new_transaction = Transaction(
            item=item,
            category_id=category_id if category_id else None,
            expense=expense,
            transaction_at=transaction_at,
            remark=remark
        )
        db.session.add(new_transaction)
        db.session.commit()
        return redirect(url_for("transactions.index"))

    # Pagination
    page = request.args.get('page', 1, type=int)
    page_size = 5
    pagination = Transaction.query.order_by(Transaction.created_at.desc()).paginate(
        page=page, 
        per_page=page_size, 
        error_out=False
    )
    return render_template(
        "transactions/index.html",
        transactions=pagination.items,
        categories=categories,
        total_pages=pagination.pages,
        current_page=pagination.page,
    )


@blueprint.route("/<int:transaction_id>", methods=["PUT"])
def update(transaction_id):
    t = Transaction.query.get_or_404(transaction_id)
    item = request.form.get("item")
    category_id = request.form.get("category")
    expense = request.form.get("expense")
    transaction_at = request.form.get("date")
    remark = request.form.get("remark")
    t.item = item
    t.category_id = category_id if category_id else None
    t.expense = expense
    t.transaction_at = transaction_at
    t.remark = remark
    db.session.commit()
    return redirect(url_for("transactions.index"))


@blueprint.route("/<int:transaction_id>", methods=["DELETE"])
def delete(transaction_id):
    t = Transaction.query.get_or_404(transaction_id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for("transactions.index"))
