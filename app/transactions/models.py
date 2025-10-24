from datetime import datetime

from .. import db


class Transaction(db.Model):
	
	__tablename__ = 'transactions'

	id = db.Column(db.Integer, primary_key=True)
	item = db.Column(db.String(128), nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('transaction_categories.id', ondelete='SET NULL'), nullable=True)
	expense = db.Column(db.Integer, nullable=False)
	transaction_at = db.Column(db.DateTime, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	category = db.relationship('TransactionCategory', backref='transactions', passive_deletes=True)


class TransactionCategory(db.Model):
	
	__tablename__ = 'transaction_categories'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
