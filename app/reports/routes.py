from flask import Blueprint, render_template, jsonify, request
from sqlalchemy import func
from datetime import date, timedelta

from . import blueprint
from app.transactions.models import Transaction, TransactionCategory


@blueprint.route('/')
def index():
    return render_template('reports/index.html')


# Helper for range filter
def filter_by_range(query, range_type):
	today = date.today()
	if range_type == 'week':
		start = today - timedelta(days=today.weekday())
		end = start + timedelta(days=6)
		query = query.filter(
			func.date(Transaction.transaction_at) >= start,
			func.date(Transaction.transaction_at) <= end
		)
	else:  # month (default)
		start = today.replace(day=1)
		if today.month == 12:
			next_month = today.replace(year=today.year+1, month=1, day=1)
		else:
			next_month = today.replace(month=today.month+1, day=1)
		end = next_month - timedelta(days=1)
		query = query.filter(
			func.date(Transaction.transaction_at) >= start,
			func.date(Transaction.transaction_at) <= end
		)
	return query


# API endpoint for expenses trend
@blueprint.route('/expenses-trend')
def get_expenses_trend():
	range_type = request.args.get('range', 'month')
	query = Transaction.query
	query = filter_by_range(query, range_type)
	results = (
		query
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
	range_type = request.args.get('range', 'month')
	query = Transaction.query
	query = filter_by_range(query, range_type)
	total = query.with_entities(func.sum(Transaction.expense)).scalar() or 0
	return jsonify({"total_expenses": int(total)})


# API endpoint for expenses breakdown by category
@blueprint.route('/expenses-breakdown')
def get_expenses_breakdown():
	range_type = request.args.get('range', 'month')
	query = Transaction.query
	query = filter_by_range(query, range_type)
	results = (
		query
		.join(TransactionCategory, Transaction.category_id == TransactionCategory.id)
		.with_entities(TransactionCategory.name, func.sum(Transaction.expense))
		.group_by(TransactionCategory.name)
		.all()
	)
	labels = [name for name, _ in results]
	data = [int(total) for _, total in results]
	return jsonify({"labels": labels, "data": data})