# System Design

System Design document helps us to realize the feature, architecture of the project.

## Technical Stacks

### Primary Language
- **Python**: 3.x (Runtime environment)

### Frameworks & Libraries
- **Web Framework**: Flask (3.1.2) - lightweight WSGI web application framework.
- **ORM**: SQLAlchemy (2.0.44) with Flask-SQLAlchemy (3.1.1) - for database interactions.
- **Database Migrations**: Alembic (1.17.0) with Flask-Migrate (4.1.0) - for handling database schema changes.
- **Template Engine**: Jinja2 (3.1.6) - for rendering HTML templates.
- **Database Driver**: psycopg2-binary (2.9.11) - PostgreSQL adapter for Python.

## Architecture

### Repository Tree

```
.
├── config.py
├── Dockerfile
├── README.md
├── requirements.txt
├── run.py
├── __pycache__/
├── app/
│   ├── __init__.py
│   ├── reports/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── static/
│   │   └── img/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── reports/
│   │   │   ├── expenses_breakdown.html
│   │   │   ├── expenses_trend.html
│   │   │   ├── index.html
│   │   │   ├── mom_comparison.html
│   │   │   ├── month_projection.html
│   │   │   └── total_expenses.html
│   │   └── transactions/
│   │       ├── index.html
│   │       └── transaction_modal.html
│   └── transactions/
│       ├── __init__.py
│       ├── models.py
│       └── routes.py
├── docs/
│   ├── roadmap.md
│   └── system.md
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
└── scripts/
    ├── seed_data.py
    └── partitions/
        └── batch_create_2026.sql
```

## Business Domain

The application is organized into modular components under the `app/` directory.

### 1. Transactions Module (`app/transactions`)

Responsible for the core ledger functionality.

- **Models**:
  - `Transaction`: Records individual expense items, including amount, date, remark, and associated category.
  - `TransactionCategory`: Defines categories for grouping expenses (e.g., Food, Transport).

- **Features**:
  - **Transaction Management**: Create and update transaction records.
  - **Listing & Filtering**: View paginated lists of transactions with support for:
    - Text search (item name).
    - Category filtering.
    - Date filtering.

### 2. Reports Module (`app/reports`)

Provides analytical views and summaries of financial data.

- **Features**:
  - **Total Expenses**: API to retrieve the total expense amount for a specific month.
  - **Month Projection**: Estimates the end-of-month total based on current spending rate (linear projection).
  - **MoM Comparison (Month-over-Month)**: Compares the current month's spending against the previous month, calculating percentage change.
  - **Expenses Breakdown**: Aggregates expenses by category for visualization (e.g., pie charts).
  - **Expenses Trend**: Aggregates expenses by date to show daily spending trends over the course of a month.