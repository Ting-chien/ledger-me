# ledger-me

LedgerMe is a Web App to track my income/expense, investment and any financial activities 😎

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

## Database Migration

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