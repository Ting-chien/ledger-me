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

    # 篩選參數
    search_text = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    date_filter = request.args.get('date', '')

    # 基礎查詢
    query = Transaction.query

    # 文字篩選 (item 欄位)
    if search_text:
        query = query.filter(Transaction.item.contains(search_text))

    # 分類篩選
    if category_filter:
        query = query.filter(Transaction.category_id == category_filter)

    # 日期篩選
    if date_filter:
        query = query.filter(Transaction.transaction_at == date_filter)

    # Pagination
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    pagination = query.order_by(Transaction.transaction_at.desc()).paginate(
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
        search_text=search_text,
        category_filter=category_filter,
        date_filter=date_filter,
    )


@blueprint.route("/<int:transaction_id>", methods=["PUT"])
def update(transaction_id):
    t = Transaction.query.get_or_404(transaction_id)
    
    # Form data extraction
    item = request.form.get("item")
    category_id = request.form.get("category")
    expense = request.form.get("expense")
    transaction_at = request.form.get("date")
    remark = request.form.get("remark")

    # Validation
    if not item or not expense or not transaction_at:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        expense_val = int(expense)
    except ValueError:
        return jsonify({"error": "Expense must be a number"}), 400

    # Update fields
    t.item = item
    t.category_id = category_id if category_id else None
    t.expense = expense_val
    t.transaction_at = transaction_at
    t.remark = remark
    
    db.session.commit()
    
    return jsonify({
        "success": True, 
        "transaction": {
            "id": t.id,
            "item": t.item,
            "category_id": t.category_id,
            "expense": t.expense,
            "date": t.transaction_at.strftime('%Y-%m-%d'),
            "remark": t.remark
        }
    })


@blueprint.route("/<int:transaction_id>", methods=["DELETE"])
def delete(transaction_id):
    t = Transaction.query.get_or_404(transaction_id)
    db.session.delete(t)
    db.session.commit()
    return '', 204
