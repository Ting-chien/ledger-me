# ledger-me

LedgerMe is a Web App to track my income/expense, investment and any financial activities 😎

Current module includes:
- Home Page: No content yet
- Transaction Page: Add, edit, delete, view transactions
- Report Page: See expenses breakdown by categories and days in a month

## Quick Start

### Prerequisites

- Python 3.11 or newer
- pip

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set environment variables

Please ask information to the project owner.

### Run the application

```bash
flask run
```

### Database Migration

1. Remember to import your models in `migrations/env.py` to enable Alembic to detect model changes.
2. Run `flask db upgrade` directly when running in a new environment.

```bash
# Step 1. Initialize migration environment (only once)
flask db init          

# Step 2. Create a new migration
flask db migrate -m "Add your migration message here"

# Step 3. Apply the migration to the database
flask db upgrade
```

## History

Table of changes made to the project.

| Date       | Version | Description                                                                                                                                                         |
| ---------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-01-19 | 1.2.0   | * Enhance Report page (Month Nav, MoM, Projection)<br>* Unify Transaction page UI integration<br>* Add seed data script                                             |
| 2025-12-12 | 1.1.0   | * Add partition table for transactions<br>* Update log system in gunicorn<br>* Update sort key in transaction page<br>* Update pagination logic in transaction page |
| 2025-11-13 | 1.0.2   | * Add history table in README.md                                                                                                                                    |
