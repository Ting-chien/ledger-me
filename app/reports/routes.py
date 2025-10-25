from flask import Blueprint, render_template, jsonify
from sqlalchemy import func

from . import blueprint
from app.transactions.models import Transaction, TransactionCategory


@blueprint.route('/')
def index():
    return render_template('reports/index.html')


# API endpoint for expenses trend
@blueprint.route('/expenses-trend')
def get_expenses_trend():
	results = (
		Transaction.query
		.with_entities(
			func.date(Transaction.transaction_at).label('date'),
			func.sum(Transaction.expense).label('total_expense')
		)
		.group_by(func.date(Transaction.transaction_at))
		.order_by(func.date(Transaction.transaction_at))
		.all()
	)
	chart_labels = [r.date.strftime('%Y-%m-%d') for r in results]
	chart_data = [int(r.total_expense) for r in results]
	return jsonify({"labels": chart_labels, "data": chart_data})


# API endpoint for total expenses
@blueprint.route('/total-expenses')
def get_total_expenses():
	total = Transaction.query.with_entities(func.sum(Transaction.expense)).scalar() or 0
	return jsonify({"total_expenses": int(total)})


# API endpoint for expenses breakdown by category
@blueprint.route('/expenses-breakdown')
def get_expenses_breakdown():
	results = (
		Transaction.query
		.join(TransactionCategory, Transaction.category_id == TransactionCategory.id)
		.with_entities(TransactionCategory.name, func.sum(Transaction.expense))
		.group_by(TransactionCategory.name)
		.all()
	)
	labels = [name for name, _ in results]
	data = [int(total) for _, total in results]
	return jsonify({"labels": labels, "data": data})