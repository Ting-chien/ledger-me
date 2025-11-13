from flask import Blueprint, render_template, jsonify
from sqlalchemy import func
from datetime import date, timedelta

from . import blueprint
from app.transactions.models import Transaction, TransactionCategory


@blueprint.route('/')
def index():
    return render_template('reports/index.html')


def get_current_month_range():
	"""取得當月的起始和結束日期"""
	today = date.today()
	start = today.replace(day=1)
	if today.month == 12:
		next_month = today.replace(year=today.year+1, month=1, day=1)
	else:
		next_month = today.replace(month=today.month+1, day=1)
	end = next_month - timedelta(days=1)
	return start, end


# API endpoint for total expenses
@blueprint.route('/total-expenses')
def get_total_expenses():
	start, end = get_current_month_range()
	total = (
		Transaction.query
		.filter(
			func.date(Transaction.transaction_at) >= start,
			func.date(Transaction.transaction_at) <= end
		)
		.with_entities(func.sum(Transaction.expense))
		.scalar() or 0
	)
	return jsonify({"total_expenses": int(total)})


# API endpoint for expenses breakdown by category
@blueprint.route('/expenses-breakdown')
def get_expenses_breakdown():
	start, end = get_current_month_range()
	results = (
		Transaction.query
		.filter(
			func.date(Transaction.transaction_at) >= start,
			func.date(Transaction.transaction_at) <= end
		)
		.join(TransactionCategory, Transaction.category_id == TransactionCategory.id)
		.with_entities(TransactionCategory.name, func.sum(Transaction.expense))
		.group_by(TransactionCategory.name)
		.all()
	)
	labels = [name for name, _ in results]
	data = [int(total) for _, total in results]
	return jsonify({"labels": labels, "data": data})


# API endpoint for expenses trend
@blueprint.route('/expenses-trend')
def get_expenses_trend():
	start, end = get_current_month_range()
	
	# 查詢當月所有有交易的日期和金額
	results = (
		Transaction.query
		.filter(
			func.date(Transaction.transaction_at) >= start,
			func.date(Transaction.transaction_at) <= end
		)
		.with_entities(
			func.date(Transaction.transaction_at).label('date'),
			func.sum(Transaction.expense).label('total_expense')
		)
		.group_by(func.date(Transaction.transaction_at))
		.order_by(func.date(Transaction.transaction_at))
		.all()
	)
	
	# 建立當月所有日期的字典，預設值為 0
	expenses_dict = {}
	current_date = start
	while current_date <= end:
		expenses_dict[current_date] = 0
		current_date += timedelta(days=1)
	
	# 填入實際有交易的日期金額
	for r in results:
		expenses_dict[r.date] = int(r.total_expense)
	
	# 轉換為 labels 和 data
	chart_labels = [d.strftime('%m/%d') for d in sorted(expenses_dict.keys())]
	chart_data = [expenses_dict[d] for d in sorted(expenses_dict.keys())]
	
	return jsonify({"labels": chart_labels, "data": chart_data})