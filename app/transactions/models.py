from datetime import datetime

from .. import db

class Transaction(db.Model):
	
	__tablename__ = 'transactions'

	id = db.Column(db.Integer, primary_key=True)
	item = db.Column(db.String(128), nullable=False)
	type = db.Column(db.String(64), nullable=False)
	expense = db.Column(db.Integer, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
