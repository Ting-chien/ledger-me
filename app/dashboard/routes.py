from flask import render_template, jsonify, request
from sqlalchemy import func
from datetime import date, timedelta
import calendar

from . import blueprint
from app.transactions.models import Transaction, TransactionCategory


@blueprint.route('/')
def index():
    return render_template('dashboard/index.html')


def get_month_range(year=None, month=None):
    """取得指定月份的起始和結束日期，若無指定則為當月"""
    try:
        if year and month:
            year = int(year)
            month = int(month)
        else:
            today = date.today()
            year = today.year
            month = today.month
    except (ValueError, TypeError):
        today = date.today()
        year = today.year
        month = today.month

    # 該月第一天
    start = date(year, month, 1)
    # 該月最後一天
    _, last_day = calendar.monthrange(year, month)
    end = date(year, month, last_day)
    return start, end


@blueprint.route('/total-expenses')
def get_total_expenses():
    year = request.args.get('year')
    month = request.args.get('month')
    start, end = get_month_range(year, month)

    total = (
        Transaction.query
        .filter(
            func.date(Transaction.transaction_at) >= start,
            func.date(Transaction.transaction_at) <= end,
            Transaction.type == 'expense'
        )
        .with_entities(func.sum(Transaction.expense))
        .scalar() or 0
    )
    return jsonify({"total_expenses": int(total)})


@blueprint.route('/total-income')
def get_total_income():
    year = request.args.get('year')
    month = request.args.get('month')
    start, end = get_month_range(year, month)

    total = (
        Transaction.query
        .filter(
            func.date(Transaction.transaction_at) >= start,
            func.date(Transaction.transaction_at) <= end,
            Transaction.type == 'income'
        )
        .with_entities(func.sum(Transaction.expense))
        .scalar() or 0
    )
    return jsonify({"total_income": int(total)})


@blueprint.route('/total-balance')
def get_total_balance():
    year = request.args.get('year')
    month = request.args.get('month')
    start, end = get_month_range(year, month)

    income = (
        Transaction.query
        .filter(
            func.date(Transaction.transaction_at) >= start,
            func.date(Transaction.transaction_at) <= end,
            Transaction.type == 'income'
        )
        .with_entities(func.sum(Transaction.expense))
        .scalar() or 0
    )
    
    expenses = (
        Transaction.query
        .filter(
            func.date(Transaction.transaction_at) >= start,
            func.date(Transaction.transaction_at) <= end,
            Transaction.type == 'expense'
        )
        .with_entities(func.sum(Transaction.expense))
        .scalar() or 0
    )
    
    balance = int(income) - int(expenses)
    return jsonify({"balance": balance, "income": int(income), "expenses": int(expenses)})


@blueprint.route('/month-projection')
def get_month_projection():
    year_arg = request.args.get('year')
    month_arg = request.args.get('month')
    start, end = get_month_range(year_arg, month_arg)
    
    # 計算該月目前累積
    current_total = (
        Transaction.query
        .filter(
            func.date(Transaction.transaction_at) >= start,
            func.date(Transaction.transaction_at) <= end,
            Transaction.type == 'expense'
        )
        .with_entities(func.sum(Transaction.expense))
        .scalar() or 0
    )
    current_total = int(current_total)

    today = date.today()
    # 只有當查詢的是「正在進行中的月份」才做預估
    if start.year == today.year and start.month == today.month:
        days_passed = today.day
        total_days = end.day
        if days_passed > 0:
            projection = (current_total / days_passed) * total_days
        else:
            projection = current_total
        return jsonify({
            "projection": int(projection),
            "is_current_month": True,
            "days_remaining": total_days - days_passed
        })
    else:
        # 過去或未來的月份，預估值就等於實際值
        return jsonify({
            "projection": current_total,
            "is_current_month": False,
            "days_remaining": 0
        })


@blueprint.route('/mom-comparison')
def get_mom_comparison():
    year_arg = request.args.get('year')
    month_arg = request.args.get('month')
    
    # 當月範圍
    start, end = get_month_range(year_arg, month_arg)
    
    # 上個月範圍
    # 計算上個月的第一天
    prev_month_date = start - timedelta(days=1)
    prev_start, prev_end = get_month_range(prev_month_date.year, prev_month_date.month)

    # 查詢當月總額
    current_total = (
        Transaction.query
        .filter(
            func.date(Transaction.transaction_at) >= start,
            func.date(Transaction.transaction_at) <= end,
            Transaction.type == 'expense'
        )
        .with_entities(func.sum(Transaction.expense))
        .scalar() or 0
    )
    
    # 查詢上月總額
    prev_total = (
        Transaction.query
        .filter(
            func.date(Transaction.transaction_at) >= prev_start,
            func.date(Transaction.transaction_at) <= prev_end,
            Transaction.type == 'expense'
        )
        .with_entities(func.sum(Transaction.expense))
        .scalar() or 0
    )

    current_total = int(current_total)
    prev_total = int(prev_total)
    
    diff_amount = current_total - prev_total
    if prev_total > 0:
        diff_percent = (diff_amount / prev_total) * 100
    else:
        diff_percent = 100 if current_total > 0 else 0
        
    return jsonify({
        "current_total": current_total,
        "prev_total": prev_total,
        "diff_amount": diff_amount,
        "diff_percent": round(diff_percent, 1)
    })


@blueprint.route('/expenses-breakdown')
def get_expenses_breakdown():
    year = request.args.get('year')
    month = request.args.get('month')
    start, end = get_month_range(year, month)

    results = (
        Transaction.query
        .filter(
            func.date(Transaction.transaction_at) >= start,
            func.date(Transaction.transaction_at) <= end,
            Transaction.type == 'expense'
        )
        .join(TransactionCategory, Transaction.category_id == TransactionCategory.id)
        .with_entities(TransactionCategory.name, func.sum(Transaction.expense))
        .group_by(TransactionCategory.name)
        .all()
    )
    labels = [name for name, _ in results]
    data = [int(total) for _, total in results]
    return jsonify({"labels": labels, "data": data})


@blueprint.route('/expenses-trend')
def get_expenses_trend():
    year = request.args.get('year')
    month = request.args.get('month')
    start, end = get_month_range(year, month)
    
    # 查詢當月所有有交易的日期和金額
    results = (
        Transaction.query
        .filter(
            func.date(Transaction.transaction_at) >= start,
            func.date(Transaction.transaction_at) <= end,
            Transaction.type == 'expense'
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


@blueprint.route('/top-expenses')
def get_top_expenses():
    year = request.args.get('year')
    month = request.args.get('month')
    start, end = get_month_range(year, month)
    
    # 查詢當月前5筆最高金額的支出
    results = (
        Transaction.query
        .filter(
            func.date(Transaction.transaction_at) >= start,
            func.date(Transaction.transaction_at) <= end,
            Transaction.type == 'expense'
        )
        .order_by(Transaction.expense.desc())
        .limit(5)
        .all()
    )
    
    data = [{
        'item': t.item,
        'expense': int(t.expense),
        'category': t.category.name if t.category else 'N/A',
        'date': t.transaction_at.strftime('%Y-%m-%d') if t.transaction_at else 'N/A'
    } for t in results]
    
    return jsonify({"top_expenses": data})
